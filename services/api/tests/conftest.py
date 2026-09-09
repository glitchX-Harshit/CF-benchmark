import pytest
from app.evaluation.types import ScenarioInput

@pytest.fixture
def sample_scenario():
    return ScenarioInput(
        industry="Software",
        prospect_role="CTO",
        company_context={"size": "enterprise"},
        prospect_context={"pain": "slow deployment"},
        objection="It costs too much right now.",
        hidden_concern=["budget constraints", "implementation time"],
        desired_outcome=["faster deployment", "lower cost"],
        expected_strategy=["focus on ROI"]
    )
