import re
from .types import DimensionResult, ScenarioInput

def score_objection_recognition(response: str, scenario: ScenarioInput) -> DimensionResult:
    objection_words = [w.lower() for w in re.findall(r'\b\w+\b', scenario.objection) if len(w) > 3]
    response_lower = response.lower()
    
    matches = sum(1 for w in objection_words if w in response_lower)
    score = 0.0
    reasoning = "Did not recognize the objection."
    evidence = "No matching keywords found."
    
    if matches > 0:
        score = min(5.0, (matches / max(1, len(objection_words))) * 5.0 * 1.5)
        reasoning = f"Recognized objection partially ({matches} keywords matched)."
        evidence = f"Found keywords related to objection."
        if score > 4.0:
            reasoning = "Strong recognition of the objection."
            evidence = "Response directly addresses key terms in the objection."
    
    return DimensionResult(dimension="objection_recognition", score=score, reasoning=reasoning, evidence=evidence)

def score_empathy(response: str, scenario: ScenarioInput) -> DimensionResult:
    empathy_keywords = ["understand", "hear", "sense", "appreciate", "valid", "completely", "see why"]
    matches = sum(1 for w in empathy_keywords if w in response.lower())
    score = min(5.0, matches * 1.5)
    return DimensionResult(dimension="empathy", score=score, reasoning=f"Detected {matches} empathy markers.", evidence="Validating language.")

def score_relevance(response: str, scenario: ScenarioInput) -> DimensionResult:
    score = 3.0
    if scenario.prospect_role.lower() in response.lower() or scenario.industry.lower() in response.lower():
        score += 2.0
    return DimensionResult(dimension="relevance", score=min(5.0, score), reasoning="Basic relevance.", evidence="Text analysis.")

def score_objection_coverage(response: str, scenario: ScenarioInput) -> DimensionResult:
    length_score = min(5.0, len(response.split()) / 20.0)
    return DimensionResult(dimension="objection_coverage", score=length_score, reasoning="Coverage based on depth.", evidence="Response length/depth.")

def score_value_articulation(response: str, scenario: ScenarioInput) -> DimensionResult:
    value_words = ["roi", "value", "save", "increase", "reduce", "grow", "efficiency"]
    matches = sum(1 for w in value_words if w in response.lower())
    return DimensionResult(dimension="value_articulation", score=min(5.0, matches * 1.5), reasoning="Value check.", evidence="Value language.")

def score_differentiation(response: str, scenario: ScenarioInput) -> DimensionResult:
    diff_words = ["unlike", "better", "unique", "only we", "compared to"]
    matches = sum(1 for w in diff_words if w in response.lower())
    return DimensionResult(dimension="differentiation", score=min(5.0, matches * 2.0), reasoning="Diff check.", evidence="Diff language.")

def score_credibility(response: str, scenario: ScenarioInput) -> DimensionResult:
    cred_words = ["data", "study", "customers", "proven", "results"]
    matches = sum(1 for w in cred_words if w in response.lower())
    return DimensionResult(dimension="credibility", score=min(5.0, matches * 2.0), reasoning="Cred check.", evidence="Cred language.")

def score_persuasion(response: str, scenario: ScenarioInput) -> DimensionResult:
    persuasion_words = ["imagine", "opportunity", "critical", "important"]
    matches = sum(1 for w in persuasion_words if w in response.lower())
    return DimensionResult(dimension="persuasion", score=min(5.0, matches * 1.5), reasoning="Persuasion check.", evidence="Persuasion language.")

def score_resistance_risk(response: str, scenario: ScenarioInput) -> DimensionResult:
    pushy_words = ["must", "have to", "now", "wrong", "deal"]
    matches = sum(1 for w in pushy_words if w in response.lower())
    score = max(0.0, 5.0 - (matches * 1.5))
    return DimensionResult(dimension="resistance_risk", score=score, reasoning="Resistance check.", evidence="Pushy language check.")

def score_next_step_quality(response: str, scenario: ScenarioInput) -> DimensionResult:
    next_step_words = ["next", "call", "schedule", "meeting", "discuss", "tomorrow", "week"]
    matches = sum(1 for w in next_step_words if w in response.lower())
    return DimensionResult(dimension="next_step_quality", score=min(5.0, matches * 1.5), reasoning="Next step check.", evidence="Action language.")
