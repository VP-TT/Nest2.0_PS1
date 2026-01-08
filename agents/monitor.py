import numpy as np

class MonitorAgent:
    def __init__(self, df, name="MonitorAgent"):
        self.df = df
        self.name = name

    def run(self):
        avg_dqi = float(self.df["Smart_DQI_Noisy"].mean())
        total_patients = len(self.df)

        high_risk_count = int((self.df["Smart_Risk_Noisy"] == "High").sum())
        high_risk_pct = round(high_risk_count / total_patients * 100, 1)

        sae_total = int(self.df["SAE_Pending_Count"].sum())
        overdue_total = int(self.df["Overdue_Visits_Count"].sum())
        missing_total = int(self.df["Missing_Pages"].sum())

        critical_sites = int(
            (self.df.groupby("Site ID")["SAE_Pending_Count"].sum() > 10).sum()
        )

        return {
            "Avg_DQI": round(avg_dqi, 2),
            "Total_Patients": total_patients,
            "High_Risk_Count": high_risk_count,
            "High_Risk_Pct": high_risk_pct,
            "SAE_Pending_Total": sae_total,
            "Overdue_Visits_Total": overdue_total,
            "Missing_Pages_Total": missing_total,
            "Critical_Site_Count": critical_sites
        }
