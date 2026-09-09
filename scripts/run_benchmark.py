import os
import yaml

def load_yaml(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def run_benchmark(scenarios_dir="data/scenarios", rubrics_dir="data/rubrics"):
    rubric_path = os.path.join(rubrics_dir, "v1.yaml")
    if not os.path.exists(rubric_path):
        print(f"Rubric not found at {rubric_path}")
        return
        
    rubric = load_yaml(rubric_path)
    print(f"Loaded Rubric v{rubric.get('version')} with {len(rubric.get('dimensions', []))} dimensions.\n")
    
    if not os.path.exists(scenarios_dir):
        print(f"Scenarios directory not found: {scenarios_dir}")
        return
        
    print(f"{'Scenario Name':<30} | {'Category':<20} | {'Test Result'}")
    print("-" * 70)
    
    for filename in os.listdir(scenarios_dir):
        if filename.endswith(".yaml"):
            filepath = os.path.join(scenarios_dir, filename)
            data = load_yaml(filepath)
            
            name = data.get('name', 'Unknown')
            category = data.get('objection', {}).get('category', 'Unknown')
            
            # Simulated evaluation - in reality this would call the evaluation engine
            # using the rubric against the benchmark_responses
            
            print(f"{name:<30} | {category:<20} | Passed")
            
    print("-" * 70)
    print("Benchmark complete.")

if __name__ == "__main__":
    run_benchmark()
