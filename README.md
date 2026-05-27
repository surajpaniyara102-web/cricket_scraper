# Cricket Scraping System

A Python-based scraping system designed to monitor and track cricket match schedules and detailed live match insights from CREX.

## Features
- Scrapes upcoming match schedules (Teams, Timings, and Context).
- Tracks individual match details (Match Info, Squads, Live Scores, and Scorecards).
- Fallback system logs data locally as JSON in case of network or ISP database blocks.

## Tech Stack
- Python 3
- BeautifulSoup4 & Requests
- PyMongo (MongoDB Atlas Cloud integration)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd cricket_scraper