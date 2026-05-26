import pytest
from agents.validator import run
from schemas.validator_output import ValidatorOutput, ToolResult

@pytest.mark.unit
def test_validator_run_returns_tuple(monkeypatch):
    # Tool must be one of 'ruff', 'pytest', 'tsc'
    mock_tool = ToolResult(tool="ruff", passed=True, return_code=0)
    monkeypatch.setattr("agents.validator.run_ruff", lambda x: mock_tool)
    monkeypatch.setattr("agents.validator.run_pytest", lambda x: mock_tool)
    monkeypatch.setattr("agents.validator.run_tsc", lambda x: mock_tool)
    output, meta = run()
    assert isinstance(output, ValidatorOutput)
    assert isinstance(meta, dict)
