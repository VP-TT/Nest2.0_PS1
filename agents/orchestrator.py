import pandas as pd
from .monitor import MonitorAgent
from .rootcause import RootCauseAgent
from .bottleneck import BottleneckAgent
from .predict import PredictAgent
from .alert import AlertAgent
from .fix_action import FixActionAgent
from .adaptive import AdaptiveAgent
from .memory import save_snapshot, load_last_n

class Orchestrator:
    def __init__(self, df, model=None, features=None, prev_df=None):
        self.df = df
        self.model = model
        self.features = features
        self.prev_df = prev_df

    def run_all(self):
        prev_runs = load_last_n(5)

        monitor_result = MonitorAgent(self.df).run()
        rootcause_result = RootCauseAgent(self.df).run()
        bottleneck_result = BottleneckAgent(self.df, self.prev_df).run()

        if self.model is not None and self.features is not None:
            predict_result = PredictAgent(self.df, self.model, self.features).run()
        else:
            predict_result = {"status": "No model loaded"}

        result = {
            "monitor": monitor_result,
            "rootcause": rootcause_result,
            "bottleneck": bottleneck_result,
            "predict": predict_result
        }

        trend_info = {}
        if prev_runs:
            try:
                dqi_vals = [x["monitor"]["Avg_DQI"] for x in prev_runs if "monitor" in x]
                if len(dqi_vals) > 1:
                    trend_info["DQI_Trend_5_Runs"] = round(dqi_vals[-1] - dqi_vals[0], 2)
            except:
                pass
            try:
                sae_vals = [x["monitor"]["SAE_Pending_Total"] for x in prev_runs if "monitor" in x]
                if len(sae_vals) > 1:
                    trend_info["SAE_Trend_5_Runs"] = round(sae_vals[-1] - sae_vals[0], 2)
            except:
                pass
            try:
                hr_vals = [x["monitor"]["High_Risk_Count"] for x in prev_runs if "monitor" in x]
                if len(hr_vals) > 1:
                    trend_info["High_Risk_Trend_5_Runs"] = hr_vals[-1] - hr_vals[0]
            except:
                pass

        result["trend_summary"] = trend_info

        save_snapshot(result)

        adaptive = AdaptiveAgent(AlertAgent().thresholds).run(result)
        result["adaptive"] = adaptive

        alert_result = AlertAgent(thresholds=adaptive.get("thresholds")).run(result)
        result["alerts"] = alert_result

        fix_result = FixActionAgent().run(result)
        result["fix_action"] = fix_result

        return result

def run_all(df, model=None, features=None, prev_df=None):
    return Orchestrator(df, model, features, prev_df).run_all()
