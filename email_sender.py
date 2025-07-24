import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, RECIPIENT_EMAIL

def send_revision_email(problems):
    """Send email with daily problems for revision"""
    if not problems:
        print("No problems to send")
        return False
    
    if not all([EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, RECIPIENT_EMAIL]):
        print("Email configuration incomplete. Please check your .env file.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"LeetCode Daily Revision - {len(problems)} Problems ({datetime.now().strftime('%Y-%m-%d')})"
        
        # Create HTML content
        html_content = create_styled_email_html(problems)
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        
        print(f"✓ Revision email sent successfully to {RECIPIENT_EMAIL}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to send email: {e}")
        return False

def create_styled_email_html(problems):
    """Create styled HTML content for email"""
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #2E7D32;
                margin: 0;
                font-size: 28px;
            }}
            .date {{
                color: #666;
                font-size: 16px;
                margin-top: 5px;
            }}
            .problem-card {{
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-bottom: 25px;
                overflow: hidden;
                background-color: #fafafa;
            }}
            .problem-header {{
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                padding: 15px 20px;
                font-size: 18px;
                font-weight: bold;
            }}
            .difficulty {{
                float: right;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }}
            .difficulty.easy {{
                background-color: #4CAF50;
            }}
            .difficulty.medium {{
                background-color: #FF9800;
            }}
            .difficulty.hard {{
                background-color: #F44336;
            }}
            .problem-content {{
                padding: 20px;
            }}
            .section {{
                margin-bottom: 20px;
            }}
            .section h3 {{
                color: #2E7D32;
                border-bottom: 2px solid #E8F5E8;
                padding-bottom: 5px;
                margin-bottom: 10px;
                font-size: 16px;
            }}
            .code-block {{
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 15px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                overflow-x: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            .explanation {{
                background-color: #e8f5e9;
                border-left: 4px solid #4CAF50;
                padding: 15px;
                border-radius: 0 4px 4px 0;
                font-style: italic;
            }}
            .leetcode-link {{
                display: inline-block;
                background-color: #FF6F00;
                color: white;
                padding: 8px 16px;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 10px;
                font-weight: bold;
            }}
            .leetcode-link:hover {{
                background-color: #E65100;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
                color: #666;
                font-size: 14px;
            }}
            .stats {{
                background-color: #E3F2FD;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 LeetCode Daily Revision</h1>
                <div class="date">{datetime.now().strftime('%A, %B %d, %Y')}</div>
            </div>
            
            <div class="stats">
                <strong>Today's Revision: {len(problems)} Problem(s)</strong>
            </div>
    '''
    
    for i, problem in enumerate(problems, 1):
        difficulty_class = problem['difficulty'].lower() if problem['difficulty'] else 'medium'
        
        html += f'''
            <div class="problem-card">
                <div class="problem-header">
                    Problem {i}: {problem['title']}
                    <span class="difficulty {difficulty_class}">{problem['difficulty']}</span>
                </div>
                <div class="problem-content">
                    <div class="section">
                        <h3>📝 Problem Description</h3>
                        <div style="color: #555; line-height: 1.5;">
                            {problem.get('statement_md', 'Problem description not available')}
                        </div>
                        <a href="https://leetcode.com/problems/{problem['slug']}/" class="leetcode-link" target="_blank">
                            View on LeetCode →
                        </a>
                    </div>
                    
                    <div class="section">
                        <h3>💻 Your Solution ({problem['language']})</h3>
                        <div class="code-block">{problem['code']}</div>
                    </div>
                    
                    <div class="section">
                        <h3>🔍 Code Analysis</h3>
                        <div class="explanation">
                            {problem.get('explanation', 'Code analysis not available')}
                        </div>
                    </div>
                    
                    <div class="section">
                        <h3>🏷️ Topics</h3>
                        <div style="color: #666;">
                            {problem.get('topics', 'Topics not available')}
                        </div>
                    </div>
                </div>
            </div>
        '''
    
    html += f'''
            <div class="footer">
                <p>Keep practicing! 💪 Consistency is the key to mastering algorithms.</p>
                <p style="color: #999; font-size: 12px;">
                    This email was automatically generated by your LeetCode Revision Agent<br>
                    Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html

def test_email_configuration():
    """Test email configuration"""
    if not all([EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, RECIPIENT_EMAIL]):
        print("✗ Email configuration incomplete")
        return False
    
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.quit()
        print("✓ Email configuration test successful")
        return True
    except Exception as e:
        print(f"✗ Email configuration test failed: {e}")
        return False

def send_test_email():
    """Send a test email"""
    test_problems = [{
        'id': 1,
        'title': 'Two Sum',
        'slug': 'two-sum',
        'difficulty': 'Easy',
        'topics': 'Array, Hash Table',
        'statement_md': 'This is a test problem for email configuration.',
        'code': 'def twoSum(nums, target):\n    # Test code\n    return []',
        'language': 'Python',
        'explanation': 'This is a test explanation.'
    }]
    
    return send_revision_email(test_problems)
