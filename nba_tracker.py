import requests
import pandas as pd

# Step 1: Define the ownership data
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

# Step 2: Fetch NBA standings from the API
url = "https://api-basketball.p.rapidapi.com/standings"
headers = {
    "X-RapidAPI-Key": "ba2b0a22f1msh3b5560778cb9864p16258fjsnd3419144186a",
    "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
}
params = {"season": "2024-2025", "league": "12"}
response = requests.get(url, headers=headers, params=params)
data = response.json()

standings_list = data['response'][0]

# Step 3: Convert standings data to DataFrame
standings_df = pd.DataFrame([
    {
        "Team": team['team']['name'],
        "Wins": team['games']['win']['total'],
        "Losses": team['games']['lose']['total']
    }
    for team in standings_list
])

# Step 4: Save the team-level win-loss data to a CSV
standings_df.to_csv("team_win_loss.csv", index=False)
print("Team win-loss data saved to team_win_loss.csv")

# Step 5: Merge standings with owner data
merged_df = pd.merge(standings_df, owners_df, on="Team", how="inner")

# Step 6: Calculate total wins by owner
owner_win_counts = merged_df.groupby("Owner")["Wins"].sum().reset_index()
owner_win_counts = owner_win_counts.sort_values(by="Wins", ascending=False)

# Step 7: Save the owner win counts to a separate CSV
owner_win_counts.to_csv("owner_win_counts.csv", index=False)
print("Owner win counts saved to owner_win_counts.csv")

# Step 8: Print results to confirm
print("\nWins by Owner:")
print(owner_win_counts)

print("\nTeam Win-Loss Data:")
print(standings_df)
