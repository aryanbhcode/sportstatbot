import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats

def fetch_season_stats(season: str) -> pd.DataFrame:
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="PerGame"
    )
    df = stats.get_data_frames()[0]
    return df


if __name__ == "__main__":
    df = fetch_season_stats("2023-24")
    print(df[["PLAYER_NAME", "TEAM_ABBREVIATION", "PTS", "AST", "REB"]].head(10))
    print(df.shape)
