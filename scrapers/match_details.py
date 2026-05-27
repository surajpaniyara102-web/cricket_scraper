import requests
from bs4 import BeautifulSoup

def scrape_match_page(match_url):
    """Scrapes detailed info, squads, live data, and scorecard from the match URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(match_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to access match page: {match_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize empty structures for the required sections
    match_info = {}
    squads = {}
    live_score = {}
    scorecard = {}

    try:
        # 1. Match Info Tab Data Extraction
        info_section = soup.find('div', class_='match-info-tab')
        if info_section:
            details = info_section.find_all('div', class_='info-row')
            for row in details:
                label = row.find('span', class_='label').text.strip()
                value = row.find('span', class_='value').text.strip()
                match_info[label] = value

        # 2. Squads Tab Data Extraction
        squad_section = soup.find('div', class_='squads-tab')
        if squad_section:
            teams = squad_section.find_all('div', class_='team-squad')
            for team in teams:
                team_name = team.find('h3').text.strip()
                players = [p.text.strip() for p in team.find_all('span', class_='player-name')]
                squads[team_name] = players

        # 3. Live Tab Data Extraction (Active when match is live)
        live_section = soup.find('div', class_='live-tab')
        if live_section:
            live_score['current_score'] = live_section.find('div', class_='score').text.strip() if live_section.find('div', class_='score') else "N/A"
            live_score['batsmen'] = [b.text.strip() for b in live_section.find_all('span', class_='batsman-name')]
            live_score['bowler'] = live_section.find('span', class_='bowler-name').text.strip() if live_section.find('span', class_='bowler-name') else "N/A"

        # 4. Scorecard Tab Data Extraction
        scorecard_section = soup.find('div', class_='scorecard-tab')
        if scorecard_section:
            # Basic structural extraction for runs/wickets breakdown
            innings = scorecard_section.find_all('div', class_='innings-accordion')
            for index, inning in enumerate(innings):
                title = inning.find('div', class_='innings-title').text.strip()
                scorecard[f"innings_{index+1}"] = {"title": title, "rows": []}

    except Exception as e:
        print(f"Parsing error on match details: {e}")

    return {
        "match_url": match_url,
        "match_info": match_info,
        "squads": squads,
        "live_score": live_score,
        "scorecard": scorecard
    }