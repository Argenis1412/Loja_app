"""
agents/executor.py

Executor — tercer agente del pipeline.

Routing por risk_level:
  LOW    → Gemini Flash ejecuta el cambio
  MEDIUM → Groq (Llama 3) ejecuta el cambio
  HIGH   → Claude Sonnet genera el diff, pero NO escribe (pending_human_review)

Contrato:
  Input  : ArchitectOutput (desde archivo JSON o directamente)
  Output : ExecutorOutput  (cambios aplicados + diff + costo)
"""
from __future__ import annotations

import difflib
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import anthropic
from google import genai
from google.genai import types
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from schemas.architect_output import ArchitectOutput, Task
from schemas.executor_output import ExecutorOutput, FileChange

load_dotenv()

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
MODEL_GEMINI = "gemini-2.5-flash"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL_GROQ = "llama-3.3-70b-versatile"

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL_CLAUDE = "claude-sonnet-4-6"
COST_PER_1M_INPUT_CLAUDE = 3.00
COST_PER_1M_OUTPUT_CLAUDE = 15.00

TIMEOUT_SECONDS = 60
MAX_RETRIES = 1

PROJECT_ROOT = Path(
    os.getenv("PROJECT_ROOT", str(Path(__file__).resolve().parent.parent.parent))
)

LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------

logger = logging.getLogger("executor")
logger.setLevel(logging.DEBUG)

_handler = logging.FileHandler(LOGS_DIR / "executor.log", encoding="utf-8")
_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)
logger.addHandler(_handler)
logging.getLogger("httpx").setLevel(logging.WARNING)

# ---------------------------------------------------------------------------
# Helpers Modelos
# ---------------------------------------------------------------------------

def _build_prompt(task: Task, file_path: Path, file_content: str) -> str:
    return f"""You are a precise code editor. Apply exactly one change to the file below.

TASK
----
Title       : {task.title}
Description : {task.description}
File        : {file_path}

RULES (mandatory)
-----------------
1. Return ONLY the complete modified file content.
2. Do NOT include markdown code fences (``` or ~~~).
3. Do NOT include any explanation, comments, or preamble.
4. Do NOT change anything outside the scope of the task.
5. If the change is already applied, return the file as-is.

FILE CONTENT
------------
{file_content}
"""

def _strip_markdown(content: str) -> str:
    if content.startswith("```"):
        parts = content.split("```")
        if len(parts) >= 3:
            content = parts[1]
            if "\n" in content:
                content = content.split("\n", 1)[1]
    return content.strip()

def _call_gemini(prompt: str, run_id: str) -> tuple[str, int, int]:
    client = genai.Client(api_key=GOOGLE_API_KEY)
    logger.debug("[%s] Gemini request | model=%s | prompt_chars=%d",
                 run_id, MODEL_GEMINI, len(prompt))

    t0 = time.perf_counter()
    response = client.models.generate_content(
        model=MODEL_GEMINI,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0)
    )
    elapsed = time.perf_counter() - t0
    
    content = _strip_markdown(response.text)
    
    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage else 0
    output_tokens = usage.candidates_token_count if usage else 0

    logger.info("[%s] Gemini OK | latency=%.2fs | in=%d | out=%d",
                run_id, elapsed, input_tokens, output_tokens)

    return content, input_tokens, output_tokens


def _call_groq(prompt: str, run_id: str) -> tuple[str, int, int]:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_GROQ,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
    }

    logger.debug("[%s] Groq request | model=%s | prompt_chars=%d",
                 run_id, MODEL_GROQ, len(prompt))

    t0 = time.perf_counter()
    with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
        response = client.post(
            f"{GROQ_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()

    elapsed = time.perf_counter() - t0
    data = response.json()

    content = _strip_markdown(data["choices"][0]["message"]["content"])
    
    usage = data.get("usage", {})
    input_tokens = usage.get("prompt_tokens", 0)
    output_tokens = usage.get("completion_tokens", 0)
    
    logger.info("[%s] Groq OK | latency=%.2fs | in=%d | out=%d",
                run_id, elapsed, input_tokens, output_tokens)

    return content, input_tokens, output_tokens


def _call_claude(prompt: str, run_id: str) -> tuple[str, int, int]:
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    logger.debug("[%s] Claude request | model=%s | prompt_chars=%d",
                 run_id, MODEL_CLAUDE, len(prompt))

    t0 = time.perf_counter()
    response = client.messages.create(
        model=MODEL_CLAUDE,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    elapsed = time.perf_counter() - t0
    
    content = _strip_markdown(response.content[0].text)

    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    logger.info("[%s] Claude OK | latency=%.2fs | in=%d | out=%d",
                run_id, elapsed, input_tokens, output_tokens)

    return content, input_tokens, output_tokens


# ---------------------------------------------------------------------------
# Core: aplicar task
# ---------------------------------------------------------------------------

def _apply_task(task: Task, run_id: str) -> FileChange:
    if not task.files_to_modify:
        logger.warning("[%s] Task %s sin files_to_modify — skip", run_id, task.task_id)
        return FileChange(
            task_id=task.task_id, file="", status="error", error="files_to_modify vacío"
        )

    relative_path = task.files_to_modify[0]
    file_path = PROJECT_ROOT / relative_path

    if not file_path.exists():
        msg = f"Archivo no encontrado: {file_path}"
        logger.error("[%s] %s", run_id, msg)
        return FileChange(
            task_id=task.task_id, file=relative_path, status="error", error=msg
        )

    original_content = file_path.read_text(encoding="utf-8")
    prompt = _build_prompt(task, file_path, original_content)

    modified_content: str | None = None
    input_tokens = output_tokens = 0
    cost_this_call = 0.0

    for attempt in range(MAX_RETRIES + 1):
        try:
            if task.risk_level == "low":
                raw, input_tokens, output_tokens = _call_gemini(prompt, run_id)
                cost_this_call = 0.0
            elif task.risk_level == "medium":
                raw, input_tokens, output_tokens = _call_groq(prompt, run_id)
                cost_this_call = 0.0
            elif task.risk_level == "high":
                raw, input_tokens, output_tokens = _call_claude(prompt, run_id)
                cost_this_call = (input_tokens / 1_000_000) * COST_PER_1M_INPUT_CLAUDE + (output_tokens / 1_000_000) * COST_PER_1M_OUTPUT_CLAUDE
            else:
                raise ValueError(f"Unknown risk level: {task.risk_level}")

            if not raw:
                raise ValueError("Respuesta vacía del modelo")

            modified_content = raw
            break

        except (httpx.HTTPError, ValueError, anthropic.APIError) as exc:
            # Capturamos excepciones generales
            logger.warning("[%s] Intento %d/%d fallido para task %s: %s",
                           run_id, attempt + 1, MAX_RETRIES + 1, task.task_id, exc)
            if attempt == MAX_RETRIES:
                return FileChange(
                    task_id=task.task_id,
                    file=relative_path,
                    status="error",
                    error=str(exc),
                    tokens_used=input_tokens + output_tokens,
                    cost_usd=cost_this_call,
                )

    assert modified_content is not None

    diff = _make_diff(original_content, modified_content, relative_path)
    
    if not diff:
        logger.info("[%s] Task %s — sin cambios (idempotente)", run_id, task.task_id)
        return FileChange(
            task_id=task.task_id, file=relative_path, status="applied",
            diff="(sin cambios — ya aplicado)", tokens_used=input_tokens + output_tokens, cost_usd=cost_this_call
        )

    if task.risk_level == "high":
        logger.info("[%s] Task %s — DIFF GENERADO (HIGH risk, no escrito)", run_id, task.task_id)
        return FileChange(
            task_id=task.task_id, file=relative_path, status="pending_human_review",
            diff=diff, tokens_used=input_tokens + output_tokens, cost_usd=cost_this_call
        )
    else:
        file_path.write_text(modified_content, encoding="utf-8")
        logger.info("[%s] Task %s — APLICADO en %s", run_id, task.task_id, relative_path)
        return FileChange(
            task_id=task.task_id, file=relative_path, status="applied",
            diff=diff, tokens_used=input_tokens + output_tokens, cost_usd=cost_this_call
        )

def _make_diff(original: str, modified: str, filename: str) -> str:
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)

    diff_lines = list(
        difflib.unified_diff(
            original_lines, modified_lines,
            fromfile=f"a/{filename}", tofile=f"b/{filename}",
            lineterm="",
        )
    )
    return "".join(diff_lines)

# ---------------------------------------------------------------------------
# Entrypoint público
# ---------------------------------------------------------------------------

def execute(architect_output: ArchitectOutput) -> ExecutorOutput:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:6]
    logger.info("=== Executor run %s ===", run_id)

    model_string = f"GM:{MODEL_GEMINI}|GQ:{MODEL_GROQ}|CL:{MODEL_CLAUDE}"
    result = ExecutorOutput(model=model_string, run_id=run_id)

    for task in architect_output.implementation_plan:
        logger.info("[%s] Task %s | risk=%s | title=%s",
                    run_id, task.task_id, task.risk_level, task.title)

        for file_relative in task.files_to_modify:
            single_file_task = task.model_copy(update={"files_to_modify": [file_relative]})
            change = _apply_task(single_file_task, run_id)
            
            result.total_tokens += change.tokens_used
            result.total_cost_usd += change.cost_usd

            if change.status == "applied":
                result.applied.append(change)
            elif change.status == "pending_human_review":
                result.pending_review.append(change)
            else:
                result.errors.append(change)

    output_path = LOGS_DIR / f"executor_{run_id}.json"
    output_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    
    logger.info(
        "[%s] Finalizado | applied=%d | pending_review=%d | errors=%d | cost=$%.6f | log=%s",
        run_id, len(result.applied), len(result.pending_review), len(result.errors),
        result.total_cost_usd, output_path.name
    )

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python agents/executor.py <architect_output.json>")
        sys.exit(1)

    architect_json_path = Path(sys.argv[1])
    if not architect_json_path.exists():
        print(f"No existe: {architect_json_path}")
        sys.exit(1)

    architect_data = json.loads(architect_json_path.read_text(encoding="utf-8"))
    architect_output = ArchitectOutput.model_validate(architect_data)

    output = execute(architect_output)

    print(f"\n[OK] Aplicados   : {len(output.applied)}")
    print(f"[~] Pending review : {len(output.pending_review)}")
    print(f"[X] Errores     : {len(output.errors)}")
    print(f"[$] Costo total : ${output.total_cost_usd:.6f}")

    if output.applied:
        print("\n--- Diffs aplicados ---")
        for change in output.applied:
            print(f"\n[{change.task_id}] {change.file}")
            print(change.diff)

    if output.pending_review:
        print("\n--- Diffs PENDIENTES (HIGH risk, no escritos) ---")
        for change in output.pending_review:
            print(f"\n[{change.task_id}] {change.file}")
            print(change.diff)
