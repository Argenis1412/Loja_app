import pytest
from agents.validator import run
from schemas.validator_output import ValidatorOutput

@pytest.mark.unit
def test_validator_run_returns_tuple(monkeypatch):
    monkeypatch.setattr("agents.validator.run_ruff", lambda x: True)
    monkeypatch.setattr("agents.validator.run_pytest", lambda x: True)
    monkeypatch.setattr("agents.validator.run_tsc", lambda x: True)
    output, meta = run()
    assert isinstance(output, ValidatorOutput)
    assert isinstance(meta, dict)
