"""
LinkedIn AI Backend Job Scraper
Uses Apify actor: cheap_scraper/linkedin-job-scraper

Setup:
    pip install requests
    export APIFY_API_TOKEN="your_token_here"

Run:
    python linkedin_ai_backend_scraper.py
"""

import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.environ.get("APIFY_API_TOKEN")
ACTOR_ID = "cheap_scraper~linkedin-job-scraper"  # Apify uses ~ in REST URLs
RUN_SYNC_URL = f"https://api.apify.com/v2/acts/{ACTOR_ID}/run-sync-get-dataset-items"

# Search terms tuned to your AI backend positioning.
# Each entry is (keyword, location) — edit freely.
SEARCHES = [
    ("AI backend engineer", "Hyderabad"),
    ("AI backend engineer", "India (Remote)"),
    ("LangChain developer", "Hyderabad"),
    ("LangGraph engineer", "India (Remote)"),
    ("RAG engineer", "Hyderabad"),
    ("RAG engineer", "India (Remote)"),
    ("FastAPI developer", "Hyderabad"),
    ("Python backend developer AI", "Hyderabad"),
]

OUTPUT_FILE = "ai_backend_jobs.json"


def run_search(keyword: str, location: str):
    payload = {
        "title": keyword,
        "location": location,
        "rows": 25,          # jobs per search — adjust as needed
        "publishedAt": "r604800",  # last 7 days; check actor docs for exact param name
    }
    headers = {"Content-Type": "application/json"}
    params = {"token": APIFY_TOKEN}

    resp = requests.post(RUN_SYNC_URL, params=params, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    return resp.json()


def main():
    if not APIFY_TOKEN:
        raise SystemExit("Set APIFY_API_TOKEN environment variable first.")

    all_jobs = []
    seen_urls = set()

    for keyword, location in SEARCHES:
        print(f"Searching: '{keyword}' in '{location}'...")
        try:
            jobs = run_search(keyword, location)
        except requests.HTTPError as e:
            print(f"  Failed: {e}")
            continue

        new_count = 0
        for job in jobs:
            url = job.get("jobUrl") or job.get("url") or job.get("link")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_jobs.append(job)
                new_count += 1

        print(f"  Got {len(jobs)} results, {new_count} new")
        time.sleep(2)  # be polite between actor runs

    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"\nDone. {len(all_jobs)} unique jobs saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()