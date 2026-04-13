"""LLM-as-a-judge: scores an AI response on five dimensions."""

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

DIMS = ["helpfulness", "accuracy", "coherence", "tone", "overall"]

JUDGE_PROMPT = """You are an expert evaluator assessing the quality of an AI assistant's response.

## Inputs
**User message:** {user_message}
**Reference answer:** {reference}
**AI response to evaluate:** {ai_response}

## Task
Score the AI response on each of the following dimensions using a scale of 1–5:

- **Helpfulness** — Does it actually address what the user asked?
- **Accuracy** — Is the information correct and consistent with the reference?
- **Coherence** — Is it well-structured and easy to understand?
- **Tone** — Is the tone appropriate and professional?
- **Overall** — Your overall holistic assessment.

## Scoring rubric
- 5 — Excellent
- 4 — Good, minor issues
- 3 — Adequate, notable gaps
- 2 — Poor, mostly fails
- 1 — Completely wrong or unhelpful

## Output format (follow exactly, no extra text)
HELPFULNESS: <1-5>
ACCURACY: <1-5>
COHERENCE: <1-5>
TONE: <1-5>
OVERALL: <1-5>
REASONING: <one or two sentences>"""


def evaluate(
    user_message: str,
    ai_response: str,
    reference: str | None = None,
) -> dict:
    """
    Score an AI response on five dimensions.

    Returns:
        {"helpfulness": int, "accuracy": int, "coherence": int,
         "tone": int, "overall": int, "reasoning": str}
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    judge_model = os.getenv("JUDGE_MODEL", "claude-sonnet-4-6")

    filled = JUDGE_PROMPT.format(
        user_message=user_message,
        ai_response=ai_response,
        reference=reference or "No reference provided — use your own judgment.",
    )

    message = client.messages.create(
        model=judge_model,
        max_tokens=256,
        system="You are a strict but fair evaluator. Follow the output format exactly.",
        messages=[{"role": "user", "content": filled}],
    )

    return _parse(message.content[0].text.strip())


def _parse(raw: str) -> dict:
    scores: dict = {dim: 0 for dim in DIMS}
    scores["reasoning"] = ""

    for line in raw.splitlines():
        upper = line.upper()
        for dim in DIMS:
            if upper.startswith(f"{dim.upper()}:"):
                try:
                    scores[dim] = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
        if line.upper().startswith("REASONING:"):
            scores["reasoning"] = line.split(":", 1)[1].strip()

    return scores
