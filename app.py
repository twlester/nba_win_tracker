from flask import Flask, render_template, url_for
import pandas as pd
import requests

# Initialize the Flask app
app = Flask(__name__)

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

    # Extract and format unique standings data
    standings_list = data['response'][0]
    standings_df = pd.DataFrame([
        {
            "Team": team['team']['name'],
            "Wins": team['games']['win']['total'],
            "Losses": team['games']['lose']['total']
        }
        for team in standings_list
    ]).drop_duplicates(subset=["Team"])  # Ensure no duplicate teams

    return standings_df

def calculate_owner_wins(standings_df):
    """Calculate total wins by owner."""
    # Data with teams and their owners
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

    # Merge standings with ownership data (inner join ensures matching teams only)
    merged_df = pd.merge(standings_df, owners_df, on="Team", how="inner")

    # Calculate total wins by owner
    owner_win_counts = merged_df.groupby("Owner")["Wins"].sum().reset_index()

    # Sort the owner win counts by total wins in descending order
    owner_win_counts = owner_win_counts.sort_values(by="Wins", ascending=False)

    return merged_df, owner_win_counts

@app.route("/")
def home():
    # Fetch the latest standings data and calculate owner wins
    standings_df = fetch_nba_standings()
    merged_df, owner_win_counts = calculate_owner_wins(standings_df)

    # Sort the merged team standings table by total wins in descending order
    merged_df = merged_df.sort_values(by="Wins", ascending=False)

    # Get the leader and loser
    leader = owner_win_counts.iloc[0]["Owner"]
    loser = owner_win_counts.iloc[-1]["Owner"]

    # Generate the message
    message = f"Way to go {leader}!! {loser}, you suck! Better luck next week."

    # Render the tables and message
    return render_template(
        "index.html",
        tables=[owner_win_counts.to_html(classes='data', index=False),
                merged_df.to_html(classes='data', index=False)],
        titles=["Owner Win Counts", "Team Win/Loss Data with Owners"],
        message=message
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
