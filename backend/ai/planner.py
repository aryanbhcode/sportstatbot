import os
import json
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# System prompt for AI planning
SYSTEM_PROMPT = SYSTEM_PROMPT = """
You are an NBA AI planner.

Your job:
- Read the user's question
- Decide exactly which backend function to call
- Output STRICT JSON only
- Fill at minimum the "action" and "season" keys if applicable

Allowed actions:
- "get_player_season"
- "league_leader"
- "top_players"

JSON format:
{
  "action": "...",        // one of allowed actions
  "player": "...",        // optional
  "stat": "PTS|AST|REB|STL|BLK|leader",  // use "leader" if asking for league leader
  "season": "YYYY-YY",
  "top_n": number         // optional
}

Rules:
- Do NOT explain or add extra text
- If the user asks "who led the league in PTS in 2022", return:
{
  "action": "league_leader",
  "stat": "PTS",
  "season": "2021-22"
}
- If the user asks "Top 5 rebounders 2021-22", return:
{
  "action": "top_players",
  "stat": "REB",
  "season": "2021-22",
  "top_n": 5
}
- Always respond in **strict JSON**.
"""


def ai_plan(question: str) -> dict:
    """
    Ask the AI to plan which function to call and what arguments to use.
    Always returns a dict. Handles errors gracefully.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            temperature=0
        )

        # Make sure there is at least one choice
        if not response.choices:
            return {"error": "No response from AI"}

        # Get the content safely
        content = response.choices[0].message.content
        content = content.strip()

        # Remove extra quotes if present
        if (content.startswith("'") and content.endswith("'")) or \
           (content.startswith('"') and content.endswith('"')):
            content = content[1:-1]

        # Parse JSON
        try:
            plan = json.loads(content)
            return plan
        except json.JSONDecodeError:
            return {"error": "Invalid AI plan JSON", "raw": content}

    except Exception as e:
        return {"error": f"AI request failed: {str(e)}"}
