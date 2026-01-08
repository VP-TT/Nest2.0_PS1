import os
import requests
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class AlertAgent:
    def __init__(self, name="AlertAgent", thresholds=None):
        self.name = name
        self.email = os.getenv("ALERT_EMAIL")
        self.password = os.getenv("ALERT_EMAIL_PASSWORD")
        self.to_email = os.getenv("ALERT_EMAIL_TO")
        self.slack_webhook = os.getenv("SLACK_WEBHOOK")

        default = {
            "high_risk_pct": 20,
            "sae_total": 200,
            "critical_sites": 3
        }

        self.thresholds = thresholds if thresholds else default

    def send_slack(self, text):
        if not self.slack_webhook:
            return "slack_skipped"
        try:
            payload = {"text": text}
            resp = requests.post(self.slack_webhook, json=payload)
            return "slack_sent" if resp.status_code == 200 else f"slack_error:{resp.status_code}"
        except Exception as e:
            return f"slack_exception:{e}"

    def send_email(self, subject, body):
        if not self.email or not self.password or not self.to_email:
            return "email_skipped"
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.email
            msg["To"] = self.to_email
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            return "email_sent"
        except Exception as e:
            return f"email_error:{e}"

    def run(self, ctx):
        m = ctx["monitor"]
        fired = False
        messages = []

        if m["High_Risk_Pct"] > self.thresholds["high_risk_pct"]:
            fired = True
            messages.append(f"🚨 {m['High_Risk_Pct']}% high-risk patients")

        if m["SAE_Pending_Total"] > self.thresholds["sae_total"]:
            fired = True
            messages.append(f"⚠️ {m['SAE_Pending_Total']} total unresolved SAE cases")

        if m["Critical_Site_Count"] > self.thresholds["critical_sites"]:
            fired = True
            messages.append(f"🏥 {m['Critical_Site_Count']} sites marked CRITICAL")

        if not fired:
            return {"fired": False, "alerts": []}

        alert_text = "\n".join(messages)

        return {
            "fired": True,
            "alerts": messages,
            "slack": self.send_slack(alert_text),
            "email": self.send_email("CLINICAL ALERT", alert_text)
        }
