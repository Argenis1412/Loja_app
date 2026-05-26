import pytest
from agents.scout import run
from schemas.scout_output import ScoutOutput

@pytest.mark.unit
def test_scout_run_returns_tuple(mock_gemini):
    mock_gemini.return_value = {"hotspots": [{"file": "test.py", "severity": "low"}], "summary": "s", "risks": "r", "recommended_order": ["t1"]}
    output, meta = run("target")
    assert isinstance(output, ScoutOutput)
    assert isinstance(meta, dict)

@pytest.mark.unit
def test_scout_meta_has_required_keys(mock_gemini):
    mock_gemini.return_value = {"hotspots": [{"file": "test.py", "severity": "low"}], "summary": "s", "risks": "r", "recommended_order": ["t1"]}
    _, meta = run("target")
    for key in ["tokens_input", "tokens_output", "cost_usd", "model_used"]:
        assert key in meta
