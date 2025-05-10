import requests
from bs4 import BeautifulSoup
import re

def scrape_points_and_schedule():
    crickbuzz_webpage = requests.get('https://www.cricbuzz.com/cricket-series/9237/indian-premier-league-2025/points-table').text
    soup = BeautifulSoup(crickbuzz_webpage, 'lxml')

    table = soup.find_all(['tbody'])
    header = soup.find_all('thead')

    imp_rows = table[0].find_all('tr', recursive=False)[::2]

    Teams, Mats, Wons, Losts, Tieds, NRs, Pts, NRRs = [], [], [], [], [], [], [], []

    for row in imp_rows:
        data = row.find_all('td')
        Teams.append(data[0].text.strip())
        Mats.append(data[1].text.strip())
        Wons.append(data[2].text.strip())
        Losts.append(data[3].text.strip())
        Tieds.append(data[4].text.strip())
        NRs.append(data[5].text.strip())
        Pts.append(data[6].text.strip())
        NRRs.append(data[7].text.strip())

    points_table = [
        {"Id": i, "Team": team.replace('\xa0\xa0(E)',''), "Matches": mat, "Won": won, "Lost": lost, "Tied": tied, "NR": nr, "Points": pts, "NRR": nrr}
        for i, (team, mat, won, lost, tied, nr, pts, nrr) in enumerate(zip(Teams, Mats, Wons, Losts, Tieds, NRs, Pts, NRRs))
    ]
    print(points_table)
    # Schedule scraping
    schedule_rows = table[0].find_all('tr', recursive=False)[1::2]
    schedule_table_rows = [row.find_all('tr') for row in schedule_rows]

    class Match:
        def __init__(self, team1, team2, match_no, date, result):
            self.team1 = team1
            self.team2 = team2
            self.match_no = match_no
            self.date = date
            self.result = result

    match_list = []
    n = -1
    for row_group in schedule_table_rows:
        n += 1
        for row in row_group:
            match_details = row.find_all('td', class_='text-left')
            if match_details:
                team1 = Teams[n]
                team2 = match_details[0].text.strip()
                match_no = match_details[1].text.strip()
                date = match_details[2].text.strip()
                result = match_details[3].text.strip()
                match_list.append(Match(team1, team2, match_no, date, result))

    seen = set()
    unique_matches = []
    for m in match_list:
        if m.match_no not in seen:
            seen.add(m.match_no)
            unique_matches.append(m)

    unique_matches.sort(key=lambda x: int(re.search(r'\d+', x.match_no).group()))

    schedule = [
        {"Match No": m.match_no, "Team 1": m.team1.replace('\xa0\xa0(E)',''), "Team 2": m.team2.replace('\xa0\xa0(E)',''), "Date": m.date, "Result": m.result}
        for m in unique_matches
    ]

    return points_table, schedule

# import pandas as pd
# import numpy as np
# from bs4 import BeautifulSoup
# import requests
# import re
# import pandas as pd
# import json

# crickbuzz_webpage = requests.get('https://www.cricbuzz.com/cricket-series/9237/indian-premier-league-2025/points-table').text

# soup = BeautifulSoup(crickbuzz_webpage,'lxml')

# table = soup.find_all(['tbody'])

# imp_rows = []

# rows = table[0].find_all('tr',recursive=False)
# imp_rows.extend(rows[::2])

# header = soup.find_all('thead')

# # Instead of using find_all, use find to get a single element and then access its text.
# # If you want to extract text from multiple elements, loop through them:

# h = [tag.text.strip() for tag in header[0].find_all(['td','th'])]

# # ['Teams-0', 'Mat-1', 'Won-2', 'Lost-3', 'Tied-4', 'NR-5', 'Pts-6', 'NRR-7', '']
# Teams = []
# Mats = []
# Wons = []
# Losts = []
# Tieds = []
# NRs = []
# Pts = []
# NRRs = []

# for i in imp_rows:
#   Teams.append(i.find_all('td')[0].text.strip())
#   Mats.append(i.find_all('td')[1].text.strip())
#   Wons.append(i.find_all('td')[2].text.strip())
#   Losts.append(i.find_all('td')[3].text.strip())
#   Tieds.append(i.find_all('td')[4].text.strip())
#   NRs.append(i.find_all('td')[5].text.strip())
#   Pts.append(i.find_all('td')[6].text.strip())
#   NRRs.append(i.find_all('td')[7].text.strip())


# # Convert to JSON format
# points_table = [
#     {"Id":id, "Team": team, "Matches": mat, "Won": won, "Lost": lost, "Tied": tied, "NR": nr, "Points": pts, "NRR": nrr}
#     for id, team, mat, won, lost, tied, nr, pts, nrr in zip(range(10),Teams, Mats, Wons, Losts, Tieds, NRs, Pts, NRRs)
# ]

# # Save to JSON file
# with open("points_table.json", "w") as f:
#     json.dump(points_table, f, indent=4)


# schedule_tables = []

# rows = table[0].find_all('tr',recursive=False)
# schedule_tables = rows[1::2]

# len(schedule_tables)

# schedule_table_rows = []

# for i in  schedule_tables:
#   schedule_table_rows.append(i.find_all('tr'))

# class Match:
#   def __init__(self,team1,team2,match_no,date,result):
#     self.team1 = team1
#     self.team2 = team2
#     self.match_no = match_no
#     self.date = date
#     self.result = result

# List_match = []
# n = -1
# for i in schedule_table_rows:
#     n = n + 1
#     for j in i:
#         match_details = j.find_all('td',class_='text-left')
#         if match_details:  # Ensure there are enough elements
#           team1 = Teams[n]
#           team2 = match_details[0].text.strip()
#           match_no = match_details[1].text.strip()
#           date = match_details[2].text.strip()
#           result = match_details[3].text.strip()
#           match = Match(team1, team2, match_no, date, result)
#           List_match.append(match)
        
# unique_matches = []
# unseen_matches = []

# for match in List_match:
#   if match.match_no not in unseen_matches:
#     unseen_matches.append(match.match_no)
#     unique_matches.append(match)

# # print(len(unique_matches))

# unique_matches.sort(key=lambda x: int(re.search(r'\d+', x.match_no).group()))

# # Convert to JSON format
# schedule_json = [
#     {"Match No": match.match_no, "Team 1": match.team1, "Team 2": match.team2, "Date": match.date, "Result": match.result}
#     for match in unique_matches
# ]

# # Save to JSON file
# with open("schedule.json", "w") as f:
#     json.dump(schedule_json, f, indent=4)
