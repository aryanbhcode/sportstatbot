import json
from tools.stats_engine import get_player_season, league_leader, top_players
from ai.planner import ai_plan

# --- RAG Layer ---
VALID_STATS = ["PTS", "AST", "REB", "STL", "BLK"]

def retrieve_stat(action=None, player=None, stat=None, season="2025-26", top_n=None):
    try:
        if action == "top_players":
            if stat not in VALID_STATS:
                return {"error": f"Invalid stat '{stat}' for top players"}
            return top_players(stat, season, top_n)

        elif action == "league_leader":
            if stat not in VALID_STATS:
                return {"error": f"Invalid stat '{stat}' for league leader"}
            return league_leader(stat, season)

        elif action == "get_player_season":
            return get_player_season(player, season)

        else:
            return {"error": "Could not find data"}
    except Exception as e:
        return {"error": str(e)}



def format_answer(result):
    # Error case
    if isinstance(result, dict) and "error" in result:
        return f"❌ {result['error']}"

    # Player season stats
    if isinstance(result, dict) and "stats" in result:
        lines = []
        lines.append(f"{result['player']} — {result['season']}\n")

        for stat, val in result["stats"].items():
            if stat == "FG_PCT":
                lines.append(f"• FG%: {round(val * 100, 1)}%")
            elif stat == "TEAM_ABBREVIATION":
                lines.append(f"• Team: {val}")
            else:
                lines.append(f"• {stat}: {round(val, 2)}")

        return "\n".join(lines)

    # League leader
    if isinstance(result, dict) and "leader" in result:
        l = result["leader"]
        return (
            f"{l['player']} ({l['team']})\n"
            f"• {round(l['value'], 2)} {result['stat']} per game\n"
            f"Season: {result['season']}"
        )

    # Top players list
    if isinstance(result, list):
        lines = ["Top Players:\n"]
        for i, p in enumerate(result, 1):
            lines.append(
                f"{i}. {p['player']} ({p['team']}) — {round(p['value'], 2)}"
            )
        return "\n".join(lines)

    return "No data found."


# --- Chatbot Loop ---
def main():
    print("NBA Chatbot (type 'exit' to quit)\n")
    while True:
        question = input("You: ")
        if question.lower() == "exit":
            break

        # 1️⃣ LLM generates plan
        plan = ai_plan(question)  # already a dict

        # 2️⃣ Check for errors
        if "error" in plan:
            print("Bot: AI failed to plan.")
            continue

        # 3️⃣ Call RAG layer
# 3️⃣ Call RAG layer safely
        try:
            result = retrieve_stat(
                action=plan.get("action"),
                player=plan.get("player"),
                stat=plan.get("stat"),
                season=plan.get("season", "2021-22"),
                top_n=plan.get("top_n")
            )
        except ValueError as e:
            # Catch errors like "Player not found"
            result = {"error": str(e)}


        # 4️⃣ Format & display
        answer = format_answer(result)
        print("Bot:", answer, "\n")

if __name__ == "__main__":
    main()
