import json
import os
from pathlib import Path

def load_test_cases():
    current_dir = Path(__file__).parent
    json_path = current_dir / "test_cases.json"
    
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

def main():
    print("=== Începere Setup Evaluări ===")
    cases = load_test_cases()
    print(f"S-au încărcat cu succes {len(cases)} cazuri de test.")
    print("Setup-ul inițial este complet.")

if __name__ == "__main__":
    main()