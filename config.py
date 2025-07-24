
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email Configuration
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# LeetCode Configuration
LEETCODE_SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('CSRF_TOKEN')
LEETCODE_USERNAME = os.getenv('LEETCODE_USERNAME')

# Database Configuration
DATABASE_PATH = 'data/problems.db'

# Scheduling Configuration
DAILY_PROBLEMS_COUNT = 2
DAILY_SEND_TIME = "07:00"

# Logging Configuration
LOG_FILE = 'revision_agent.log'
