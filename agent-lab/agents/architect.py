# agents/architect.py
import os
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
import anthropic
from schemas.architect_output import ArchitectOutput
from logger import log_call

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-3-5-sonnet-20241022"

COST_PER_1M_INPUT  = 3.00
COST_PER_1M_OUTPUT = 15.00

def call_claude(prompt: str, agent_label: str) -> tuple[str, dict, float]:
    """Wrapper with retry and logging for Claude."""
    for attempt in range(2):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            raw = response.content[0].text.strip()

            # Strip markdown fences if present
            if raw.startswith("```"):
                parts = raw.split("```")
                if len(parts) >= 3:
                    raw = parts[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                raw = raw.strip()

            tokens = {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens,
            }
            cost = (
                tokens["input"] / 1_000_000 * COST_PER_1M_INPUT +
                tokens["output"] / 1_000_000 * COST_PER_1M_OUTPUT
            )

            log_call(
                agent=agent_label,
                prompt=prompt[:500],
                response=raw[:500],
                tokens=tokens,
                cost_usd=cost,
            )

            return raw, tokens, cost

        except anthropic.RateLimitError:
            if attempt == 0:
                print(f"[{agent_label}] Rate limit. Waiting 60s...")
                time.sleep(60)
                continue
            raise
        except Exception as e:
            raise RuntimeError(f"[{agent_label}] Failed: {e}")

    raise RuntimeError(f"[{agent_label}] Failed after retry.")

ARCHITECT_PROMPT = """
You are the Architect Agent. Your job is to analyze the reconnaissance data provided by the Scout Agent.
Dado este diagnóstico del Scout, tu trabajo es:
1. Validar los findings — detecta falsos positivos
2. Priorizar por impacto real vs esfuerzo
3. Detectar riesgos sistémicos que el Scout no vio
4. Diseñar orden de implementación seguro
5. Identificar qué bloquea Phase 2 del Engineering Playbook

No implementes nada.
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

[OUTPUT DEL SCOUT]
{scout_data}
"""

def run(scout_output: ScoutOutput) -> tuple[ArchitectOutput, dict]:
    print(f"[Architect] Processing ScoutOutput object...")

    # Generar prompt con el objeto
    scout_data = scout_output.model_dump_json()

    print(f"[Architect] Asking {MODEL} to structure the implementation plan...")

    raw_response, tokens, cost = call_claude(
        ARCHITECT_PROMPT.format(scout_data=scout_data),
        agent_label="architect"
    )

    print(f"[Architect] Done | tokens: {tokens} | cost: ${cost:.5f}")

    # Validate JSON
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as e:
        print(f"[Architect] JSON parse error: {e}")
        print(f"[Architect] Raw output:\n{raw_response}")
        raise

    output = ArchitectOutput(**data)
    
    meta = {
        "tokens_input": tokens["input"],
        "tokens_output": tokens["output"],
        "cost_usd": cost,
        "model_used": MODEL
    }
    
    return output, meta


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agents/architect.py <path_to_scout_output.json>")
        sys.exit(1)
        
    scout_path = sys.argv[1]
    with open(scout_path, "r") as f:
        scout_data = ScoutOutput.model_validate_json(f.read())
        
    result, _ = run(scout_data)
    print("\n-- Architect Output --")
    print(json.dumps(result.model_dump(), indent=2))
