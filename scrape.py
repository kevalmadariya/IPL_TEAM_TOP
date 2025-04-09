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
        {"Id": i, "Team": team, "Matches": mat, "Won": won, "Lost": lost, "Tied": tied, "NR": nr, "Points": pts, "NRR": nrr}
        for i, (team, mat, won, lost, tied, nr, pts, nrr) in enumerate(zip(Teams, Mats, Wons, Losts, Tieds, NRs, Pts, NRRs))
    ]

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
        {"Match No": m.match_no, "Team 1": m.team1, "Team 2": m.team2, "Date": m.date, "Result": m.result}
        for m in unique_matches
    ]

    return points_table, schedule
