from leetcode_api import fetch_latest_submissions
from sent_tracker import load_sent, save_sent
from mailer import format_email, send_email
from config import DAILY_SEND_TIME
import schedule
import time

def select_unsent(submissions, sent_set):
    return [sub for sub in submissions if sub["titleSlug"] not in sent_set][:2]

def daily_job():
    print("Running daily LeetCode revision job...")
    subs = fetch_latest_submissions()
    if not subs:
        print("No problem data fetched from API. (Probably rate limit or network error.)")
        return
    sent = load_sent()
    to_send = select_unsent(subs, sent)
    if not to_send:
        print("No unsent problems found today!")
        return
    html = format_email(to_send)
    send_email("Your Daily LeetCode Revision", html)
    sent.update([p["titleSlug"] for p in to_send])
    save_sent(sent)
    print(f"Sent {len(to_send)} problems.")

def run_scheduler():
    print(f"Scheduler started. Emails will be sent daily at {DAILY_SEND_TIME}.")
    schedule.every().day.at(DAILY_SEND_TIME).do(daily_job)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # To run now for testing, uncomment next line:
    # daily_job()
    # For real schedule, comment above and uncomment below:
    run_scheduler()