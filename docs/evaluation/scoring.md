# Scoring System

The scoring system in CF Benchmark is designed to evaluate AI model responses against pre-defined rubrics.

## Methodology

Scores are calculated based on multiple criteria defined in a scenario's rubric. 
Each criterion is evaluated, often using a stronger model as an evaluator (LLM-as-a-judge), and aggregated into a final score.

### Rubric Structure
- **Dimensions**: Areas being evaluated (e.g., Accuracy, Tone, Formatting).
- **Scales**: The scoring scale (e.g., 1-5, binary).
- **Weights**: Relative importance of each dimension.
