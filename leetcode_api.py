import requests
from config import LEETCODE_USERNAME

def fetch_latest_submissions():
    url = f"https://alfa-leetcode-api.onrender.com/{LEETCODE_USERNAME}/acSubmission"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 429:
            print("\n[ERROR] Too many requests - the API has rate-limited you. "
                  "Wait 1-2 hours and try again.")
            print("This API is public and not intended for high-frequency polling.\n")
            return []
        r.raise_for_status()
        data = r.json()
        return data.get("submission", [])
    except requests.RequestException as e:
        print("\n[ERROR] Failed to fetch LeetCode submissions:", str(e), "\n")
        return []
