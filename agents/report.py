from agents.base import AgentBase
from datetime import datetime
import os
import json

class ReportAgent(AgentBase):
    """Compile daily status report summarizing all agent outputs."""

    def __init__(self, report_dir="reports"):
        super().__init__("ReportAgent")
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)

    def run(self, monitor_output=None, predict_output=None, alert_output=None, fix_output=None):
        
        # Collect sections safely
        snapshot = monitor_output.get("snapshot", "No monitor data.") if monitor_output else "No monitor."
        pred_summary = predict_output.get("summary", "No prediction data.") if predict_output else "No predict."
        alerts = alert_output.get("alerts", []) if alert_output else []
        fix_text = fix_output.get("text", "No fixes proposed.") if fix_output else "No fix."

        # Format alert block
        alert_lines = "\n".join(f"- {a['type']}: {a['message']}" for a in alerts) if alerts else "No alerts raised."

        # Build report
        report = f"""
=== NEST AI SYSTEM REPORT ===
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

📍 SYSTEM SNAPSHOT
{snapshot}

🔮 PREDICTIVE INSIGHT
{pred_summary}

🚨 ALERTS TRIGGERED
{alert_lines}

🛠️ RECOMMENDED ACTIONS
{fix_text}

=== END REPORT ===
"""

        # Save to file
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = os.path.join(self.report_dir, f"report_{ts}.txt")

        with open(fname, "w", encoding="utf-8") as f:
            f.write(report)

        self.log("Generated daily report.")

        return {
            "status": "REPORT_CREATED",
            "file": fname,
            "text": report
        }
