import json
import time
import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.progress import track
from .judge import evaluate

console = Console()

def run_batch(test_cases_path: str, output_dir: str = "results") -> str:
    Path(output_dir).mkdir(exist_ok=True)

    with open(test_cases_path) as f:
        cases = json.load(f)

    results = []
    console.print(f"\n[bold]Running evaluation on {len(cases)} test cases...[/bold]\n")

    for case in track(cases, description="Evaluating..."):
        try:
            scores = evaluate(
                user_message=case["user_message"],
                ai_response=case["ai_response"],
                reference=case.get("reference")
            )
            results.append({
                "id": case.get("id", ""),
                "user_message": case["user_message"],
                "ai_response": case["ai_response"],
                **scores
            })
            time.sleep(0.5)
        except Exception as e:
            console.print(f"[red]Error on {case.get('id')}: {e}[/red]")

    df = pd.DataFrame(results)
    output_path = f"{output_dir}/eval_results.csv"
    df.to_csv(output_path, index=False)
    console.print(f"\n[green]Results saved to {output_path}[/green]")
    return output_path