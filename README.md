## LeetCode Daily Revision Agent

This project is a fully automated Python bot that emails you **2 unsent LeetCode problems every day**, using your last 20 solved problems pulled from a public API. You get problem titles, solution links, and basic info delivered to your inbox each morning. No manual selection, no prompts—just consistent revision!

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
