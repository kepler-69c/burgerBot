import os
import tomllib
from dotenv import load_dotenv
from helpers.sendmail import GmailSend

load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
recipients = os.getenv("RECIPIENTS").split(",")

mail = GmailSend(email, password)

text = ""
html = f"""
<!DOCTYPE html>
<html lang="en">
<head></head>
<body>
    <h1>Settings changed</h1>
    <ul>
        <li><strong>send</strong>: "always"->"burger only"</li>
        <li><strong>quiet days</strong>: []->["20241221/20250221",]</li>
    </ul>
</body>
</html>
"""

mail.send_html(recipients, "test", text, html)
