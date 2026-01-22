import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
import difflib
from rapidfuzz import process, fuzz


IMPORTANT_STATS = [
    "PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "TEAM_ABBREVIATION"
]

SEASON_CACHE = {}

def normalize(text: str) -> str:
    return text.lower().strip()

def get_season_df(season: str) -> pd.DataFrame:
    if season in SEASON_CACHE:
        return SEASON_CACHE[season]

    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="PerGame"
    )
    df = stats.get_data_frames()[0]

    SEASON_CACHE[season] = df
    return df

def fuzzy_match_player(player_query, all_players_map):
    player_query = player_query.lower()
    match = process.extractOne(player_query, all_players_map.keys(), scorer=fuzz.ratio)
    
    if match and match[1] > 0:
        # match[0] is the lowercase key
        return all_players_map[match[0]]  # return original name
    return None

def get_player_season(player: str, season: str) -> dict:
    df = get_season_df(season)
    all_players = df["PLAYER_NAME"].unique().tolist()

    all_players_lower_map = {p.lower(): p for p in all_players}

    matched_player = fuzzy_match_player(player, all_players_lower_map)

    if not matched_player:
        return {"error": f"Player '{player}' not found for season {season}"}

    player_row = df[df["PLAYER_NAME"] == matched_player].iloc[0]
    player_dict = {stat: player_row[stat] for stat in IMPORTANT_STATS}

    return {
        "player": matched_player,
        "season": season,
        "stats": player_dict
    }


def league_leader(stat: str, season: str) -> dict:
    df = get_season_df(season)

    leader = df.sort_values(stat, ascending=False).iloc[0]

    return {
        "stat": stat,
        "season": season,
        "leader": {
            "player": leader["PLAYER_NAME"],
            "team": leader["TEAM_ABBREVIATION"],
            "value": float(leader[stat])
        }
    }



def top_players(stat: str, season: str, n: int) -> list:
    df = get_season_df(season)

    leaders = df.sort_values(stat, ascending=False).head(n)

    return [
        {
            "player": row["PLAYER_NAME"],
            "team": row["TEAM_ABBREVIATION"],
            "value": float(row[stat])
        }
        for _, row in leaders.iterrows()
    ]


    


if __name__ == "__main__":
    playerstats = get_player_season("Stephen Curry", "2021-22")
    print(playerstats)
    pointleader = league_leader("PTS", "2021-22")
    print(pointleader)
    topfivepoints = top_players("PTS", "2021-22", 5)
    print(topfivepoints)