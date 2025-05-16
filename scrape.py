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

    unique_matches.sort(key=lambda x: int(re.search(r'\d+', x.match_no).group()) if re.search(r'\d+', x.match_no) else float('inf'))

    schedule = [
        {"Match No": m.match_no, "Team 1": m.team1.replace('\xa0\xa0(E)',''), "Team 2": m.team2.replace('\xa0\xa0(E)',''), "Date": m.date, "Result": m.result}
        for m in unique_matches
    ]
    

    # orange cap extract
    indian_express = requests.get('https://www.livemint.com/sports/cricket-news/ipl-orange-cap').text
    soup = BeautifulSoup(indian_express,'lxml')
    orange_cap_div = soup.find_all('div',class_='orangeCapWrap')
    orange_cap_header = orange_cap_div[0].find_all('thead')
    # orange_cap_table_header =[i.text.strip() for i in orange_cap_header[0].find_all('th')]
    orange_cap_table = orange_cap_div[0].find_all('tbody')
    orange_cap_table_row = orange_cap_table[0].find_all('tr')[:15]
    orange_cap_table_row_data = []
    for i in orange_cap_table_row:
        temp = [j.text.strip() for j in i.find_all('td')]
        orange_cap_table_row_data.append(temp)
    orange_cap_list_of_directory = [{'Player':i[0],'R':i[1],'SR':i[2],'Mat':i[3],'Inn':i[4],'NO':i[5], 'HS':i[6], 'Avg':i[7], '30s':i[8], '50s':i[9] ,'100s':i[10], '6s':i[11] } for i in orange_cap_table_row_data]

    # purple cap extract
    indian_express = requests.get('https://www.livemint.com/sports/cricket-news/ipl-purple-cap').text
    soup = BeautifulSoup(indian_express,'lxml')
    purple_cap_div = soup.find_all('div',class_='tableContainer')
    purple_cap_header = purple_cap_div[0].find_all('thead')
    purple_cap_table_header = [i.text.strip() for i in purple_cap_header[0].find_all('th')]
    purple_cap_tabel = purple_cap_div[0].find_all('tbody')
    purple_cap_table_row = purple_cap_tabel[0].find_all('tr')[:15]
    purple_cap_table_row_data = []
    for i in purple_cap_table_row:
        temp = [j.text.strip() for j in i.find_all('td')]
        purple_cap_table_row_data.append(temp)
    purple_cap_list_of_directory = [{'Player':i[0], 'W':i[1], 'Avg':i[2], 'Ovr':i[3], 'R':i[4], 'BBF':i[5], 'EC':i[6], 'SR':i[7], '3w':i[8], '5w':i[9]} for i in purple_cap_table_row_data]

    return points_table, schedule, orange_cap_list_of_directory, purple_cap_list_of_directory 
