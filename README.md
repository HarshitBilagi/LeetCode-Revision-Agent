## LeetCode Daily Revision Agent

This project is a fully automated Python bot that emails you **2 unsent LeetCode problems every day**, using your last 20 solved problems pulled from a public API: https://github.com/alfaarghya/alfa-leetcode-api. You get problem titles, solution links, and basic info delivered to your inbox each morning. No manual selection, no prompts—just consistent revision!

<img width="466" height="432" alt="Screenshot 2025-09-14 183823" src="https://github.com/user-attachments/assets/821215ce-fcd3-4161-8909-ed7fbe1d6e1e" />


***

## Features

- **Fetches latest accepted submissions** for your LeetCode account from a free API
- **Selects 2 problems per day** (FIFO, never repeats until all sent)
- **Emails you the titles, links, languages, and timestamps**
- **Remembers sent problems** (local file, no repeats)
- **Easy to configure**: Just set up your username and email in `config.py`
- **Cloud friendly**: Runs as a persistent bot on Railway, Fly.io, or PythonAnywhere

***

## Getting Started

1. **Clone this repo**:
    ```
    git clone https://github.com/harshitbilagi/leetcode-revision-agent.git
    cd leetcode-revision-agent
    ```

2. **Install dependencies**:
    ```
    pip install -r requirements.txt
    ```

3. **Configure your credentials** in `config.py`:
   - `LEETCODE_USERNAME` = your LeetCode user
   - `EMAIL_USER` = your Gmail address (app password required!)
   - `EMAIL_PASS` = your Gmail app password (see docs)
   - `RECIPIENT_EMAIL` = your inbox (can be the same as above)

4. **Test locally**:
    ```
    python main.py
    ```

   > Emails you 2 new problems instantly (for testing).

## Cloud Hosting

<img width="1919" height="1015" alt="image" src="https://github.com/user-attachments/assets/dbcf05e9-3716-48b1-a909-4fe77b8b5cc8" />

<img width="1515" height="698" alt="Screenshot 2025-09-04 131902" src="https://github.com/user-attachments/assets/e1f230ba-465f-437b-ba75-9252b4e3b527" />

