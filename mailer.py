import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_USER, EMAIL_PASS, RECIPIENT_EMAIL, EMAIL_HOST, EMAIL_PORT

def format_email(problems):
    ent = []
    for p in problems:
        link = f"https://leetcode.com/problems/{p['titleSlug']}/"
        ent.append(f"""
        <h2>{p['title']} <small>({p['lang']})</small></h2>
        <p><a href="{link}">View on LeetCode</a></p>
        <p>Status: {p['statusDisplay']}, Submitted: {p['timestamp']}</p>
        <hr/>
        """)
    html = "<html><body><h1>Today's LeetCode Revision</h1>" + "".join(ent) + "</body></html>"
    return html

def send_email(subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = RECIPIENT_EMAIL
    part = MIMEText(html_body, "html")
    msg.attach(part)
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as s:
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASS)
        s.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
