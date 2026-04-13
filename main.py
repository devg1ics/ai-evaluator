from evaluator.runner import run_batch
from evaluator.metrics import summarize
from evaluator.exporter import export_excel, export_pdf

if __name__ == "__main__":
    results_path = run_batch("data/test_cases.json")
    summarize(results_path)
    export_excel(results_path)
    export_pdf(results_path)
    print("\nDone! Check results/ folder for reports.")