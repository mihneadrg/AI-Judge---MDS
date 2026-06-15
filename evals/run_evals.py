import json
import time
import sys
from pathlib import Path
from dotenv import load_dotenv

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

load_dotenv(dotenv_path=project_root / ".env")

from src.agents.pipeline import CourtPipeline

def load_test_cases():
    json_path = current_dir / "test_cases.json"
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

def main():
    print("=== Start Evaluări: Format și Latență ===\n")
    cases = load_test_cases()
    
    print("Inițializare CourtPipeline...")
    pipeline = CourtPipeline(model="llama-3.1-8b-instant")
    
    for case in cases:
        print(f"Rulare test: [{case['id']}] - {case['category']}")
        start_time = time.time()
        
        try:
            result = pipeline.judge(case['input_text'])
            
            if result.get("success") is False:
                status = f"FAILED (Eroare internă: {result.get('error')})"
            else:
                status = "PASSED"
                
        except Exception as e:
            status = f"FAILED (Eroare critică: {str(e)})"
            
        end_time = time.time()
        latency = round(end_time - start_time, 2)
        
        print(f"Status: {status} | Latență totală: {latency}s")
        print("-" * 50)
        
        time.sleep(25)

if __name__ == "__main__":
    main()