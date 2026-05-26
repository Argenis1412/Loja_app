import pytest
from agents.architect import run
from schemas.scout_output import ScoutOutput
from schemas.architect_output import ArchitectOutput

@pytest.mark.unit
def test_architect_run_returns_tuple(mock_claude):
    mock_claude.return_value = {"implementation_plan": []}
    scout_out = ScoutOutput(hotspots=[], summary="s", risks="r", recommended_order=[])
    output, meta = run(scout_out)
    assert isinstance(output, ArchitectOutput)
    assert isinstance(meta, dict)
