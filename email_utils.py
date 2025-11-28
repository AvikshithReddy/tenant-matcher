import os
import ssl
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv, find_dotenv

# Load the nearest .env file (project root)

load_dotenv(find_dotenv())

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

def send_results_email(to_email, units_df):
    if not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError(
            "SMTP_USER or SMTP_PASSWORD is not set. "
            "Check your .env file and Gmail App Password."
        )

    msg = EmailMessage()
    msg["Subject"] = f"Your matched units ({len(units_df)} results)"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    msg.set_content(
        "Hi,\n\nHere are the rental units that match your preferences.\n\n"
        "If you don't see the table, please enable HTML in your email client."
    )

    html_table = units_df.to_html(index=False)
    msg.add_alternative(f"""
        <html>
          <body>
            <p>Here are your matched units:</p>
            {html_table}
          </body>
        </html>
    """, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.set_debuglevel(1)   # <--- turn on SMTP logging while debugging
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    print(f"✅ Email sent to {to_email}")