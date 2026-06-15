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

def evaluate_quality(result_data):
    """Evaluează determinist calitatea răspunsului generat de agenți."""
    score = 0
    max_score = 3
    feedback = []

    if not result_data.get("success"):
        return 0, max_score, ["Eroare critică în pipeline (0 puncte)"]
    
    prosecution = result_data.get("prosecution", {})
    verdict = result_data.get("final_verdict", {})

    if isinstance(prosecution, dict) and "severity_level" in prosecution:
        valid_levels = ["PETTY", "MODERATE", "SEVERE"]
        if prosecution["severity_level"] in valid_levels:
            score += 1
        else:
            feedback.append(f"Severitate invalidă: {prosecution['severity_level']}")
    else:
        feedback.append("Procurorul nu a returnat câmpul 'severity_level'.")

    if isinstance(prosecution, dict) and "formal_charges" in prosecution and len(prosecution["formal_charges"]) > 0:
        score += 1
    else:
        feedback.append("Procurorul nu a generat acuzații formale.")

    if isinstance(verdict, dict) and "charges" in verdict:
        score += 1
    else:
        feedback.append("Judecătorul nu a formulat capetele de acuzare finale ('charges').")

    return score, max_score, feedback

def main():
    print("=== Start Evaluări: Format, Latență și Calitate ===\n")
    cases = load_test_cases()
    
    print("Inițializare CourtPipeline...")
    pipeline = CourtPipeline(model="llama-3.1-8b-instant")
    
    for idx, case in enumerate(cases):
        print(f"Rulare test: [{case['id']}] - {case['category']}")
        start_time = time.time()
        
        # --- LOGICA DE AUTO-RETRY ---
        max_retries = 3
        status = "FAILED"
        score_text = "N/A"
        feedback = []
        
        for attempt in range(max_retries):
            try:
                result = pipeline.judge(case['input_text'])
                
                if result.get("success") is False:
                    error_msg = str(result.get('error'))
                    # Dacă dăm de limită, punem pauză și mai încercăm o dată
                    if "429" in error_msg or "Rate limit" in error_msg:
                        print(f"  [!] Limită Groq atinsă. Pauză 30s și reîncercăm... (Încercarea {attempt+1}/{max_retries})")
                        time.sleep(30)
                        continue
                    else:
                        status = f"FAILED (Eroare internă: {error_msg})"
                        break
                else:
                    # Totul e ok, evaluăm scorul
                    status = "PASSED"
                    score, max_score, feedback = evaluate_quality(result)
                    score_text = f"{score}/{max_score}"
                    break
                    
            except Exception as e:
                status = f"FAILED (Eroare critică: {str(e)})"
                break
        # ----------------------------
        
        end_time = time.time()
        latency = round(end_time - start_time, 2)
        
        print(f"Status: {status} | Calitate logică: {score_text} | Latență: {latency}s")
        if feedback:
            print("  [!] Avertismente de calitate:")
            for f in feedback:
                print(f"      - {f}")
        print("-" * 60)
        
        # O pauză normală între teste
        if idx < len(cases) - 1:
            time.sleep(15)

if __name__ == "__main__":
    main()