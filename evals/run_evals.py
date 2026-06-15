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
    score = 0
    max_score = 3
    feedback = []

    if not result_data.get("success"):
        return 0, max_score, ["Eroare critică în pipeline (0 puncte)"]
    
    prosecution = result_data.get("prosecution", {})
    verdict = result_data.get("final_verdict", {})

    if isinstance(prosecution, dict) and "severity_level" in prosecution:
        valid_levels = ["PETTY", "MODERATE", "SEVERE", "CATASTROPHIC"]
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

def generate_markdown_report(results, total_time):
    report_path = current_dir / "evals_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Raport Evaluare AI Judge\n\n")
        f.write(f"**Timp total execuție teste:** {total_time}s\n")
        f.write(f"**Total cazuri procesate:** {len(results)}\n\n")
        f.write("| ID Caz | Categorie | Status | Scenariu | Scor Calitate | Latență (s) |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for r in results:
            f.write(f"| {r['id']} | {r['category']} | {r['status']} | {r['text']} | {r['score']} | {r['latency']} |\n")
        
        f.write("\n## Observații Erori / Feedback\n")
        has_errors = False
        for r in results:
            if r['feedback']:
                has_errors = True
                f.write(f"- **{r['id']}**: {', '.join(r['feedback'])}\n")
        if not has_errors:
            f.write("Toate testele au trecut cu scor maxim de calitate.\n")

def main():
    print("=== Start Evaluări: Format, Calitate și Raportare ===\n")
    cases = load_test_cases()
    pipeline = CourtPipeline(model="llama-3.1-8b-instant")
    
    results_log = []
    global_start = time.time()
    
    for idx, case in enumerate(cases[:3]):
        print(f"Rulare test: [{case['id']}] - {case['category']}")
        start_time = time.time()
        feedback = []
        
        max_retries = 3
        status = "FAILED"
        score_text = "N/A"
        
        for attempt in range(max_retries):
            try:
                result = pipeline.judge(case['input_text'])
                
                if result.get("success") is False:
                    error_msg = str(result.get('error'))
                    if "429" in error_msg or "Rate limit" in error_msg:
                        print(f"  [!] Limită Groq atinsă. Pauză 30s și reîncercăm... (Încercarea {attempt+1}/{max_retries})")
                        time.sleep(30)
                        continue
                    else:
                        status = f"FAILED ({error_msg})"
                        feedback.append(error_msg)
                        break
                else:
                    status = "PASSED"
                    score, max_score, eval_feedback = evaluate_quality(result)
                    score_text = f"{score}/{max_score}"
                    feedback.extend(eval_feedback)
                    break
                    
            except Exception as e:
                status = "FAILED"
                feedback.append(str(e))
                break
        
        end_time = time.time()
        latency = round(end_time - start_time, 2)
        
        results_log.append({
            "id": case['id'],
            "category": case['category'],
            "status": status,
            "text": case['input_text'][:40] + "...",
            "score": score_text,
            "latency": latency,
            "feedback": feedback
        })
        
        print(f"Status: {status} | Calitate logică: {score_text} | Latență: {latency}s")
        if feedback:
            print("  [!] Avertismente de calitate:")
            for f in feedback:
                print(f"      - {f}")
        print("-" * 60)
        
        if idx < len(cases[:3]) - 1:
            time.sleep(15)
            
    global_end = time.time()
    generate_markdown_report(results_log, round(global_end - global_start, 2))
    print("\nRaport generat cu succes în fișierul evals_report.md")

if __name__ == "__main__":
    main()