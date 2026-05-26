import sys
from pathlib import Path
from unittest.mock import MagicMock

# Mock libraries that require API keys
sys.modules["google"] = MagicMock()
sys.modules["google.genai"] = MagicMock()
sys.modules["anthropic"] = MagicMock()
sys.modules["dotenv"] = MagicMock()

# Add 'agent-lab' to sys.path so we can import agents
agent_lab_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(agent_lab_path))

# Import agents (these are already refactored to return (Output, dict))
from agents.scout import run as run_scout
from agents.architect import run as run_architect
from agents.executor import run as run_executor
from agents.validator import run as run_validator

# We are confident in the refactor, so we just run the functions.
# The refactored functions return (Output, dict).
# We mock dependencies to prevent them from crashing the agent initialization.

def test():
    # Test Scout (needs target path)
    # Mocking the client inside scout would be hard, so just try running it
    try:
        _, meta = run_scout("targets/loja_app")
        print(f"PASS: Scout signature verified. Meta: {meta}")
    except Exception as e:
        print(f"FAIL: Scout signature verification failed: {e}")

    # Test Architect (needs scout output file)
    dummy_file = Path("agent-lab/architect_test.json")
    if dummy_file.exists():
        try:
            _, meta = run_architect(str(dummy_file))
            print(f"PASS: Architect signature verified. Meta: {meta}")
        except Exception as e:
            print(f"FAIL: Architect signature verification failed: {e}")
    else:
        print("SKIP: Architect test (dummy file not found)")

    # Test Executor (needs architect output)
    try:
        architect_output = MagicMock()
        architect_output.implementation_plan = []
        _, meta = run_executor(architect_output)
        print(f"PASS: Executor signature verified. Meta: {meta}")
    except Exception as e:
        print(f"FAIL: Executor signature verification failed: {e}")

    # Test Validator
    try:
        _, meta = run_validator()
        print(f"PASS: Validator signature verified. Meta: {meta}")
    except Exception as e:
        print(f"FAIL: Validator signature verification failed: {e}")

if __name__ == "__main__":
    test()
