"""
compare_architects.py — Paso 4-5 del plan.

Corre el mismo scout_output_sample.json por Gemini Flash y Claude Sonnet,
guarda ambos outputs, y genera una comparación estructurada.

Usage:
    uv run python compare_architects.py
"""
import os
import sys
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
import anthropic

from schemas.architect_output import ArchitectOutput
from logger import log_call

load_dotenv()

SCOUT_INPUT = "scout_output_sample.json"

# ── Prompt idéntico para ambos modelos ─────────────────────────────────────
ARCHITECT_PROMPT = """
You are the Architect Agent. Your job is to analyze the reconnaissance data provided by the Scout Agent.

Given this diagnostic from the Scout, your job is:
1. Validate the findings — detect false positives
2. Prioritize by real impact vs effort
3. Detect systemic risks the Scout missed
4. Design a safe implementation order
5. Identify what blocks Phase 2 of the Engineering Playbook

Do NOT implement anything. Do NOT suggest code.
Output: ONLY valid JSON matching this exact schema. No explanation. No markdown:
{{
  "validated_findings": ["string"],
  "false_positives": ["string"],
  "systemic_risks": ["string"],
  "implementation_plan": [
    {{
      "task_id": "string",
      "title": "string",
      "description": "string",
      "files_to_modify": ["string"],
      "priority": "high|medium|low",
      "effort": "high|medium|low",
      "risk_level": "high|medium|low",
      "dependencies": ["string"]
    }}
  ],
  "blockers": ["string"]
}}

[SCOUT OUTPUT]
{scout_data}
"""


def strip_fences(raw: str) -> str:
    """Remove markdown code fences if the model wraps JSON in them."""
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        if len(parts) >= 3:
            inner = parts[1]
            if inner.startswith("json"):
                inner = inner[4:]
            return inner.strip()
    return raw


def run_gemini(prompt: str) -> tuple[str, dict, float]:
    """Call Gemini Flash and return (raw_json, tokens, cost)."""
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    print("[Gemini] calling gemini-2.5-flash ...")
    start = time.time()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    latency = round(time.time() - start, 2)
    raw = strip_fences(response.text)
    usage = response.usage_metadata
    tokens = {
        "input": usage.prompt_token_count or 0,
        "output": usage.candidates_token_count or 0,
    }
    cost = tokens["input"] / 1e6 * 0.075 + tokens["output"] / 1e6 * 0.30
    print(f"[Gemini] done in {latency}s | tokens: {tokens} | cost: ${cost:.5f}")
    log_call("architect_gemini", prompt[:500], raw[:500], tokens, cost)
    return raw, tokens, cost


def run_claude(prompt: str) -> tuple[str, dict, float]:
    """Call Claude Sonnet and return (raw_json, tokens, cost)."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    model = "claude-sonnet-4-6"
    print(f"[Claude] calling {model} ...")
    start = time.time()
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = round(time.time() - start, 2)
    raw = strip_fences(response.content[0].text)
    tokens = {
        "input": response.usage.input_tokens,
        "output": response.usage.output_tokens,
    }
    cost = tokens["input"] / 1e6 * 3.00 + tokens["output"] / 1e6 * 15.00
    print(f"[Claude] done in {latency}s | tokens: {tokens} | cost: ${cost:.5f}")
    log_call("architect_claude", prompt[:500], raw[:500], tokens, cost)
    return raw, tokens, cost


def validate_output(raw: str, label: str) -> ArchitectOutput | None:
    """Parse and validate against Pydantic schema."""
    try:
        data = json.loads(raw)
        output = ArchitectOutput(**data)
        print(f"[{label}] schema validation OK -- {len(output.implementation_plan)} tasks")
        return output
    except Exception as e:
        print(f"[{label}] schema validation FAILED: {e}")
        print(f"[{label}] raw output:\n{raw[:1000]}")
        return None


def compare(gemini_out: ArchitectOutput, claude_out: ArchitectOutput) -> dict:
    """Build a structured comparison between both outputs."""
    g_tasks = {t.task_id: t for t in gemini_out.implementation_plan}
    c_tasks = {t.task_id: t for t in claude_out.implementation_plan}

    g_files = set()
    for t in gemini_out.implementation_plan:
        g_files.update(t.files_to_modify)
    c_files = set()
    for t in claude_out.implementation_plan:
        c_files.update(t.files_to_modify)

    return {
        "gemini": {
            "task_count": len(g_tasks),
            "task_ids": list(g_tasks.keys()),
            "validated_findings": gemini_out.validated_findings,
            "false_positives": gemini_out.false_positives,
            "systemic_risks": gemini_out.systemic_risks,
            "blockers": gemini_out.blockers,
            "files_touched": sorted(g_files),
            "risk_distribution": {
                "high": sum(1 for t in g_tasks.values() if t.risk_level == "high"),
                "medium": sum(1 for t in g_tasks.values() if t.risk_level == "medium"),
                "low": sum(1 for t in g_tasks.values() if t.risk_level == "low"),
            },
        },
        "claude": {
            "task_count": len(c_tasks),
            "task_ids": list(c_tasks.keys()),
            "validated_findings": claude_out.validated_findings,
            "false_positives": claude_out.false_positives,
            "systemic_risks": claude_out.systemic_risks,
            "blockers": claude_out.blockers,
            "files_touched": sorted(c_files),
            "risk_distribution": {
                "high": sum(1 for t in c_tasks.values() if t.risk_level == "high"),
                "medium": sum(1 for t in c_tasks.values() if t.risk_level == "medium"),
                "low": sum(1 for t in c_tasks.values() if t.risk_level == "low"),
            },
        },
        "deltas": {
            "files_only_gemini": sorted(g_files - c_files),
            "files_only_claude": sorted(c_files - g_files),
            "files_both": sorted(g_files & c_files),
            "gemini_found_more_risks": len(gemini_out.systemic_risks) > len(claude_out.systemic_risks),
            "claude_found_false_positives": len(claude_out.false_positives) > len(gemini_out.false_positives),
        },
    }


def main():
    # Load scout data
    scout_path = Path(SCOUT_INPUT)
    if not scout_path.exists():
        print(f"❌ {SCOUT_INPUT} not found. Run the scout first.")
        sys.exit(1)

    scout_data = scout_path.read_text(encoding="utf-8")
    prompt = ARCHITECT_PROMPT.format(scout_data=scout_data)

    print("=" * 60)
    print("ARCHITECT COMPARISON — Gemini Flash vs Claude Sonnet")
    print("=" * 60)

    # ── Run Gemini ─────────────────────────────────────────────
    print("\n--- Gemini Flash ---")
    gemini_raw, gemini_tokens, gemini_cost = run_gemini(prompt)
    gemini_out = validate_output(gemini_raw, "Gemini")

    # Save raw output
    Path("logs/architect_gemini_output.json").write_text(gemini_raw, encoding="utf-8")

    # ── Run Claude ─────────────────────────────────────────────
    print("\n--- Claude Sonnet ---")
    claude_raw, claude_tokens, claude_cost = run_claude(prompt)
    claude_out = validate_output(claude_raw, "Claude")

    # Save raw output
    Path("logs/architect_claude_output.json").write_text(claude_raw, encoding="utf-8")

    # ── Compare ────────────────────────────────────────────────
    if gemini_out and claude_out:
        print("\n" + "=" * 60)
        print("COMPARISON RESULTS")
        print("=" * 60)

        comparison = compare(gemini_out, claude_out)
        comparison["cost_comparison"] = {
            "gemini_cost": round(gemini_cost, 5),
            "claude_cost": round(claude_cost, 5),
            "ratio": round(claude_cost / gemini_cost, 1) if gemini_cost > 0 else 0,
        }

        # Save comparison
        comp_path = Path("logs/architect_comparison.json")
        comp_path.write_text(json.dumps(comparison, indent=2), encoding="utf-8")
        print(f"\n[OK] Comparison saved to {comp_path}")
        print(json.dumps(comparison, indent=2))
    else:
        print("\n[FAIL] One or both outputs failed validation. Check logs above.")
        if gemini_out:
            print("  Gemini: OK")
        if claude_out:
            print("  Claude: OK")

    print(f"\n[$$] Total cost: ${gemini_cost + claude_cost:.5f}")


if __name__ == "__main__":
    main()
