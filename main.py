import schedule
import time
import logging
from datetime import datetime
import sys
import os

# Import our modules
from database import initialize_database, add_problem, get_problems_count
from problem_selector import select_problems_for_today, get_review_statistics
from code_explainer import add_explanations_to_problems
from email_sender import send_revision_email, test_email_configuration
from database import log_reviewed_problems
from config import DAILY_SEND_TIME, LOG_FILE

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def daily_revision_job():
    """Main job function that runs at 7 AM daily"""
    logger.info("Starting daily revision job...")
    
    try:
        # 1. Select 2 problems for today
        logger.info("Selecting problems for today's revision...")
        problems = select_problems_for_today()
        
        if not problems:
            logger.warning("No problems found for today's revision")
            return
        
        logger.info(f"Selected {len(problems)} problems: {[p['title'] for p in problems]}")
        
        # 2. Generate explanations for problems that don't have them
        logger.info("Generating code explanations...")
        problems = add_explanations_to_problems(problems)
        
        # 3. Send formatted email
        logger.info("Sending revision email...")
        email_sent = send_revision_email(problems)
        
        if email_sent:
            # 4. Log the problems as reviewed
            problem_ids = [p['id'] for p in problems]
            log_reviewed_problems(problem_ids)
            logger.info(f"Successfully completed daily revision job - sent {len(problems)} problems")
        else:
            logger.error("Failed to send revision email")
        
    except Exception as e:
        logger.error(f"Error in daily revision job: {e}")

def setup_initial_data():
    """Set up initial data - add some sample problems for testing"""
    logger.info("Setting up initial sample data...")
    
    sample_problems = [
        {
            'title': 'Two Sum',
            'slug': 'two-sum',
            'difficulty': 'Easy',
            'topics': 'Array, Hash Table',
            'statement': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
            'code': '''def twoSum(self, nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []''',
            'language': 'Python'
        },
        {
            'title': 'Valid Parentheses',
            'slug': 'valid-parentheses',
            'difficulty': 'Easy',
            'topics': 'String, Stack',
            'statement': 'Given a string s containing just the characters (, ), {, }, [ and ], determine if the input string is valid.',
            'code': '''def isValid(self, s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return not stack''',
            'language': 'Python'
        },
        {
            'title': 'Binary Tree Inorder Traversal',
            'slug': 'binary-tree-inorder-traversal',
            'difficulty': 'Medium',
            'topics': 'Stack, Tree, Depth-First Search, Binary Tree',
            'statement': 'Given the root of a binary tree, return the inorder traversal of its nodes values.',
            'code': '''def inorderTraversal(self, root):
    result = []
    
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    
    inorder(root)
    return result''',
            'language': 'Python'
        }
    ]
    
    for problem in sample_problems:
        add_problem(
            problem['title'],
            problem['slug'], 
            problem['difficulty'],
            problem['topics'],
            problem['statement'],
            problem['code'],
            problem['language']
        )
    
    logger.info(f"Added {len(sample_problems)} sample problems to database")

def print_system_status():
    """Print current system status"""
    print("\n" + "="*60)
    print("📊 LEETCODE REVISION AGENT STATUS")
    print("="*60)
    
    # Database status
    try:
        problem_count = get_problems_count()
        print(f"💾 Database: {problem_count} problems stored")
    except Exception as e:
        print(f"💾 Database: Error - {e}")
    
    # Email configuration status
    print("📧 Email Configuration:", end=" ")
    if test_email_configuration():
        print("✓ READY")
    else:
        print("✗ NOT CONFIGURED")
    
    # Review statistics
    try:
        stats = get_review_statistics()
        print(f"📈 Statistics:")
        print(f"   • Total problems: {stats['total_problems']}")
        print(f"   • Reviewed today: {stats['reviewed_today']}")
        print(f"   • Never reviewed: {stats['never_reviewed']}")
    except Exception as e:
        print(f"📈 Statistics: Error - {e}")
    
    print(f"⏰ Next email: Daily at {DAILY_SEND_TIME}")
    print("="*60)

def run_scheduler():
    """Run the scheduler continuously"""
    logger.info(f"LeetCode Revision Agent started - will send daily emails at {DAILY_SEND_TIME}")
    print_system_status()
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in scheduler: {e}")
            time.sleep(60)

def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'init':
            # Initialize database and add sample data
            initialize_database()
            setup_initial_data()
            print("\n✓ System initialized with sample data")
            print("Next steps:")
            print("1. Configure your .env file with email settings")
            print("2. Run 'python main.py test-email' to test email configuration")
            print("3. Run 'python main.py' to start the scheduler")
            
        elif command == 'test-email':
            # Test email configuration
            from email_sender import send_test_email
            print("Testing email configuration...")
            if send_test_email():
                print("✓ Test email sent successfully!")
            else:
                print("✗ Test email failed. Please check your .env configuration.")
                
        elif command == 'run-now':
            # Run the daily job immediately for testing
            print("Running daily revision job now...")
            daily_revision_job()
            
        elif command == 'status':
            # Show system status
            print_system_status()
            
        elif command == 'help':
            print("LeetCode Revision Agent Commands:")
            print("  init      - Initialize database with sample data")
            print("  test-email - Send a test email")
            print("  run-now   - Run daily revision job immediately")
            print("  status    - Show system status")
            print("  help      - Show this help message")
            print("  (no args) - Start the scheduler")
            
        else:
            print(f"Unknown command: {command}")
            print("Run 'python main.py help' for available commands")
    else:
        # No arguments - start the scheduler
        # Initialize database if it doesn't exist
        initialize_database()
        
        # Schedule the daily job
        schedule.every().day.at(DAILY_SEND_TIME).do(daily_revision_job)
        
        # Run the scheduler
        run_scheduler()

if __name__ == "__main__":
    main()
