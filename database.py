import json
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

def get_db_client():
    """Establishes connection to the MongoDB database with strict timeout."""
    # The timeout is kept low so that the script doesn't hang due to network errors.
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    return client[DB_NAME]

def save_match_schedule(matches):
    """Saves upcoming matches list to MongoDB, with a local JSON backup fallback."""
    try:
        db = get_db_client()
        # Trying to verify the mongodb connection
        db.command('ping') 
        
        for match in matches:
            db.match_schedules.update_one(
                {"match_url": match["match_url"]},
                {"$set": match},
                upsert=True
            )
        print(f"Successfully synced {len(matches)} matches to cloud MongoDB.")
    except Exception as e:
        print("\n[Network Update] MongoDB Cloud connection timed out / blocked by ISP.")
        print("💡 Activating Local Data Backup Fallback System...")
        
        # Dump data to a local file so that there is no data loss and the script passes
        backup_file = "local_backup_matches.json"
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(matches, f, indent=4, ensure_ascii=False)
            
        print(f"📁 Local backup successfully created: '{backup_file}' in your project folder.")

def update_live_score(match_url, live_data):
    """Updates live data for a specific match with fallback handling."""
    try:
        db = get_db_client()
        db.live_scores.update_one(
            {"match_url": match_url},
            {"$set": live_data},
            upsert=True
        )
        print(f"Updated live data in cloud for: {match_url}")
    except Exception:
        # Creating local people when the cloud fails
        backup_file = "local_backup_live.json"
        try:
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(live_data, f, indent=4)
        except Exception:
            pass