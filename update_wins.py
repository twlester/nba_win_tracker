import pandas as pd
import requests

def fetch_nba_standings():
    """Fetch NBA standings from the API."""
    url = "https://api-basketball.p.rapidapi.com/standings"
    headers = {
        "X-RapidAPI-Key": "ba2b0a22f1msh3b5560778cb9864p16258fjsnd3419144186a",
        "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
    }
    params = {"season": "2024-2025", "league": "12"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Extract and format standings data
    standings_list = data['response'][0]
    standings_df = pd.DataFrame([
        {
            "Team": team['team']['name'],
            "Wins": team['games']['win']['total'],
            "Losses": team['games']['lose']['total']
        }
        for team in standings_list
    ])
    return standings_df

def calculate_owner_wins(standings_df):
    """Calculate total wins by owner."""
    data = {
        "Team": [
            "Philadelphia 76ers", "Milwaukee Bucks", "Chicago Bulls",
            "Cleveland Cavaliers", "Boston Celtics", "Los Angeles Clippers",
            "Memphis Grizzlies", "Atlanta Hawks", "Miami Heat",
            "Charlotte Hornets", "Utah Jazz", "Sacramento Kings",
            "New York Knicks", "Los Angeles Lakers", "Orlando Magic",
            "Dallas Mavericks", "Brooklyn Nets", "Denver Nuggets",
            "Indiana Pacers", "New Orleans Pelicans", "Detroit Pistons",
            "Toronto Raptors", "Houston Rockets", "San Antonio Spurs",
            "Phoenix Suns", "Oklahoma City Thunder", "Minnesota Timberwolves",
            "Portland Trail Blazers", "Golden State Warriors", "Washington Wizards"
        ],
        "Owner": [
            "Chris", "Ben", "Dan", "Dan", "Alex", "Ben", "Alex", "Alex", "Bill",
            "Dan", "Ben", "Alex", "Dan", "Ben", "Dan", "Bill", "Bill", "Bill",
            "Ben", "Dan", "Chris", "Chris", "Chris", "Alex", "Chris", "Ben",
            "Chris", "Bill", "Bill", "Alex"
        ]
    }
    owners_df = pd.DataFrame(data)

    # Merge standings with ownership data
    merged_df = pd.merge(standings_df, owners_df, on="Team", how="inner")

    # Calculate wins by owner
    owner_win_counts = merged_df.groupby("Owner")["Wins"].sum().reset_index()
    return owner_win_counts

def update_csv_files():
    standings_df = fetch_nba_standings()
    owner_win_counts = calculate_owner_wins(standings_df)

    # Save updated data to CSV files
    standings_df.to_csv("team_standings.csv", index=False)
    owner_win_counts.to_csv("owner_win_counts.csv", index=False)

if __name__ == "__main__":
    update_csv_files()
