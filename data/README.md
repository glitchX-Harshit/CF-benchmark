# CF Benchmark Data

This repository contains the evaluation datasets, scenarios, and rubrics for the CF Benchmark sales intelligence platform.

## Structure

- `data/scenarios/` - Contains YAML files defining different sales scenarios and objection handling challenges.
- `data/rubrics/` - Contains the evaluation rubrics used to score responses.
- `data/golden/` - Contains golden test cases with expected score ranges for regression testing.
- `scripts/` - Contains utility scripts for validating data, seeding databases, and running tests.

## Scenario Format

Each scenario is a YAML file representing a specific sales situation, including the prospect's context, the specific objection they raise, and benchmark examples of poor to excellent responses.

## Adding Scenarios

1. Create a new `.yaml` file in `data/scenarios/`.
2. Follow the exact schema defined in the system. Use `scripts/validate_dataset.py` to ensure your new scenario conforms.
3. Ensure the benchmark responses represent a clear gradient of quality according to the rubric.

## Running Utilities

```bash
# Validate all scenarios
python scripts/validate_dataset.py

# Seed the database
python scripts/seed_database.py

# Run a test benchmark
python scripts/run_benchmark.py
```
