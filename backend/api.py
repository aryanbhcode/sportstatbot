from fastapi import FastAPI, HTTPException
from tools.stats_engine import get_player_season, league_leader, top_players

app = FastAPI(title="SportStatBot API")

@app.get("/player/{player}/{season}")
def player_season(player: str, season: str):
    try:
        return get_player_season(player, season)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/leader/{stat}/{season}")
def leader(stat: str, season: str):
    return league_leader(stat.upper(), season)

@app.get("/top/{stat}/{season}")
def top_n(stat: str, season: str, n: int = 5):
    return top_players(stat.upper(), season, n)
