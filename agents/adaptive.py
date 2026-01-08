from .memory import load_last_n

class AdaptiveAgent:
    def __init__(self, alert_thresholds, name="AdaptiveAgent"):
        self.name = name
        self.thresholds = alert_thresholds

    def run(self, ctx):
        history = load_last_n(5)
        if not history or len(history) < 3:
            return {"status": "Not enough data"}

        dqi_vals = []
        sae_vals = []
        hr_vals = []

        for h in history:
            m = h.get("monitor", {})
            dqi_vals.append(m.get("Avg_DQI", 0))
            sae_vals.append(m.get("SAE_Pending_Total", 0))
            hr_vals.append(m.get("High_Risk_Count", 0))

        trend_dqi = dqi_vals[-1] - dqi_vals[0]
        trend_hr = hr_vals[-1] - hr_vals[0]
        trend_sae = sae_vals[-1] - sae_vals[0]

        adjustment = "no_change"

        if trend_dqi < -5 or trend_hr > 10 or trend_sae > 50:
            self.thresholds["high_risk_pct"] = max(10, self.thresholds["high_risk_pct"] - 2)
            self.thresholds["sae_total"] = max(50, self.thresholds["sae_total"] - 20)
            adjustment = "tightened"

        elif trend_dqi > 5 and trend_hr < -5:
            self.thresholds["high_risk_pct"] = min(30, self.thresholds["high_risk_pct"] + 2)
            self.thresholds["sae_total"] = min(500, self.thresholds["sae_total"] + 20)
            adjustment = "relaxed"

        return {
            "thresholds": self.thresholds.copy(),
            "adjustment": adjustment,
            "trend": {
                "DQI": trend_dqi,
                "HighRisk": trend_hr,
                "SAE": trend_sae
            }
        }
