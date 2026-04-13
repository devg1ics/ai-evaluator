import pandas as pd
from rich.table import Table
from rich.console import Console

console = Console()

def summarize(results_path: str):
    df = pd.read_csv(results_path)
    dims = ["helpfulness", "accuracy", "coherence", "tone", "overall"]
    for d in dims:
        if d in df.columns:
            df[d] = pd.to_numeric(df[d], errors="coerce").fillna(0).astype(int)

    table = Table(title="Evaluation Summary", show_header=True)
    table.add_column("Dimension", style="bold")
    table.add_column("Mean", justify="right")
    table.add_column("Min", justify="right")
    table.add_column("Max", justify="right")
    table.add_column("Pass Rate (>=4)", justify="right")

    for dim in dims:
        col = df[dim]
        pass_rate = f"{(col >= 4).mean() * 100:.0f}%"
        table.add_row(
            dim.capitalize(),
            f"{col.mean():.2f}",
            str(int(col.min())),
            str(int(col.max())),
            pass_rate
        )

    console.print(table)

    worst = df.nsmallest(3, "overall")[["id", "user_message", "overall", "reasoning"]]
    console.print("\n[bold red]Worst performing cases:[/bold red]")
    for _, row in worst.iterrows():
        console.print(f"\n  [{row['id']}] Score: {row['overall']}/5")
        console.print(f"  Q: {str(row['user_message'])[:80]}")
        console.print(f"  Reason: {str(row['reasoning'])[:120]}")