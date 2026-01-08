from agents.base import AgentBase
from datetime import datetime
from ollama import chat
import json
import os

class FixAgent(AgentBase):
    """Propose remediation actions using a small open-source LLM."""
    
    def __init__(self, model="llama3.2", fix_dir="fixes"):
        super().__init__("FixAgent")
        self.model = model
        self.fix_dir = fix_dir
        os.makedirs(fix_dir, exist_ok=True)

    def suggest(self, issues, predictions):
        """Generate a recommended plan using LLM."""
        
        issues_txt = "\n".join(f"- {i}" for i in issues)
        preds_txt = json.dumps(predictions, indent=2)

        prompt = f"""
You are a Clinical Trial Data Operations Expert.
Suggest actions ONLY related to:
- Improving data quality
- Clearing pending SAE backlogs
- Reducing overdue visits
- Monitoring Study 4 if necessary
- Avoid medical advice

Given:
TODAY PROBLEMS:
{issues_txt}

PREDICTED FUTURE RISKS (top 10 patients):
{preds_txt}

Provide:
1. Top 3 operational fixes
2. Which studies/sites to focus on
3. Expected effect on risk and DQI
4. Short-term vs long-term steps

Do NOT invent numbers.
Just describe what must happen operationally.
"""

        response = chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

    def run(self, monitor_output=None, predict_output=None):
        if not monitor_output and not predict_output:
            self.log("No data passed to FixAgent.")
            return {"status": "NO_INPUT"}
        
        issues = monitor_output.get("issues", []) if monitor_output else []
        predictions = predict_output.get("top_predictions", []) if predict_output else []

        if not issues and not predictions:
            self.log("No active issues to fix.")
            return {"status": "OK", "fix": "No action required."}

        summary = self.suggest(issues, predictions)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = os.path.join(self.fix_dir, f"fix_{ts}.txt")

        with open(fname, "w", encoding="utf-8") as f:
            f.write(summary)

        self.log("Generated remediation plan.")

        return {
            "status": "FIX_PROPOSED",
            "file": fname,
            "text": summary
        }
