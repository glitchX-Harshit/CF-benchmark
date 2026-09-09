import os
import yaml
from jsonschema import validate, ValidationError

schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "version": {"type": "string"},
        "name": {"type": "string"},
        "prospect": {
            "type": "object",
            "properties": {
                "role": {"type": "string"},
                "industry": {"type": "string"},
                "company_size": {"type": "string"},
                "sales_stage": {"type": "string"}
            },
            "required": ["role", "industry", "company_size", "sales_stage"]
        },
        "context": {
            "type": "object",
            "properties": {
                "current_solution": {"type": "string"},
                "pain_points": {"type": "array", "items": {"type": "string"}},
                "additional_context": {"type": "string"}
            },
            "required": ["current_solution", "pain_points"]
        },
        "objection": {
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "explicit": {"type": "string"},
                "hidden_concern": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["category", "explicit", "hidden_concern"]
        },
        "desired_outcome": {"type": "array", "items": {"type": "string"}},
        "expected_strategy": {"type": "array", "items": {"type": "string"}},
        "undesired_behavior": {"type": "array", "items": {"type": "string"}},
        "evaluation": {
            "type": "object",
            "properties": {
                "key_dimensions": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["key_dimensions"]
        },
        "benchmark_responses": {
            "type": "object",
            "properties": {
                "poor": {"type": "string"},
                "weak": {"type": "string"},
                "average": {"type": "string"},
                "strong": {"type": "string"},
                "excellent": {"type": "string"}
            },
            "required": ["poor", "weak", "average", "strong", "excellent"]
        }
    },
    "required": ["id", "version", "name", "prospect", "context", "objection", "desired_outcome", "expected_strategy", "undesired_behavior", "evaluation", "benchmark_responses"]
}

def validate_dataset(scenarios_dir="data/scenarios"):
    all_valid = True
    if not os.path.exists(scenarios_dir):
        print(f"Directory not found: {scenarios_dir}")
        return False
        
    for filename in os.listdir(scenarios_dir):
        if filename.endswith(".yaml"):
            filepath = os.path.join(scenarios_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = yaml.safe_load(f)
                validate(instance=data, schema=schema)
                print(f"Valid: {filename}")
            except ValidationError as e:
                print(f"Invalid: {filename} - {e.message}")
                all_valid = False
            except Exception as e:
                print(f"Error reading {filename}: {str(e)}")
                all_valid = False
                
    return all_valid

if __name__ == "__main__":
    is_valid = validate_dataset()
    if not is_valid:
        exit(1)
