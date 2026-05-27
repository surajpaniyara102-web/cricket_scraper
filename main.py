import time
from scrapers.schedule import fetch_upcoming_matches
from scrapers.match_details import scrape_match_page
from database import save_match_schedule, update_live_score

def run_pipeline():
    print("--- Starting Cricket Scraper System ---")
    
    # Step 1: Fetch and save the match schedules
    print("Fetching match schedules...")
    upcoming_matches = fetch_upcoming_matches()
    if upcoming_matches:
        save_match_schedule(upcoming_matches)
    
    # Step 2: Loop through matches to fetch live details if active
    print("Checking details for tracked matches...")
    for match in upcoming_matches:
        url = match.get("match_url")
        if url:
            print(f"Scraping detailed data for: {match['team1']} vs {match['team2']}")
            detailed_data = scrape_match_page(url)
            if detailed_data:
                update_live_score(url, detailed_data)
            
            # Politeness delay to prevent getting blocked by CREX
            time.sleep(2)

if __name__ == "__main__":
    run_pipeline()