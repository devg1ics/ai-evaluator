import os
import json
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

DIMENSIONS = ["helpfulness", "accuracy", "coherence", "tone"]

def build_prompt(user_message: str, ai_response: str, reference: str = None) -> str:
    ref_section = f"\nReference answer: {reference}" if reference else ""
    dims = "\n".join([f"- {d}: score 1-5" for d in DIMENSIONS])
    return f"""You are an expert evaluator of AI chatbot responses.
Score the AI response on these dimensions:
{dims}

User message: {user_message}
AI response: {ai_response}{ref_section}

Return ONLY valid JSON (no markdown, no extra text):
{{"helpfulness":<1-5>,"accuracy":<1-5>,"coherence":<1-5>,"tone":<1-5>,"overall":<1-5>,"reasoning":"<explanation>"}}"""


def evaluate(user_message: str, ai_response: str, reference: str = None) -> dict:
    prompt = build_prompt(user_message, ai_response, reference)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.content[0].text.strip()
    return json.loads(raw)