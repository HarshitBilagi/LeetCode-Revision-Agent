import os
# from dotenv import load_dotenv

# load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# LEETCODE_SESSION = os.getenv('LEETCODE_SESSION')
# CSRF_TOKEN = os.getenv('CSRF_TOKEN')
LEETCODE_USERNAME = os.getenv('LEETCODE_USERNAME')

DAILY_PROBLEMS_COUNT = 2 
DAILY_SEND_TIME = "07:00"

# LOG_FILE = 'revision_agent.log'