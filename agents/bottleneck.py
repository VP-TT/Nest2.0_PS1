import pandas as pd

class BottleneckAgent:
    def __init__(self, df, prev_df=None, name="BottleneckAgent"):
        self.df = df
        self.prev_df = prev_df
        self.name = name

    def run(self):
        df = self.df
        insights = {}

        try:
            study_means = df.groupby("Study")["Smart_DQI_Noisy"].mean().sort_values()
            worst_study = study_means.index[0]
            insights["Worst_Study"] = worst_study
            insights["Worst_Study_Avg_DQI"] = round(study_means.iloc[0], 2)
        except Exception:
            insights["Worst_Study"] = None
            worst_study = None

        try:
            if worst_study:
                sub = df[df["Study"] == worst_study]
                site_means = sub.groupby("Site ID")["Smart_DQI_Noisy"].mean().sort_values()
                insights["Worst_Site"] = int(site_means.index[0])
                insights["Worst_Site_DQI"] = round(site_means.iloc[0], 2)
                gap = round(site_means.max() - site_means.min(), 2)
                insights["Intra_Study_Variation"] = gap
        except Exception:
            pass

        try:
            overall = df.agg({
                "SAE_Pending_Count": "mean",
                "Overdue_Visits_Count": "mean",
                "Missing_Pages": "mean"
            })
            sub = df[df["Study"] == worst_study] if worst_study else df
            worst = sub.agg({
                "SAE_Pending_Count": "mean",
                "Overdue_Visits_Count": "mean",
                "Missing_Pages": "mean"
            })
            diffs = (worst - overall).sort_values(ascending=False).round(2)
            insights["Key_Drivers"] = diffs.to_dict()
            insights["Primary_Driver"] = diffs.index[0]
        except Exception:
            pass

        try:
            offenders = df.groupby("Study").mean()[[
                "SAE_Pending_Count",
                "Overdue_Visits_Count",
                "Missing_Pages"
            ]]
            systemic = []
            for col in offenders.columns:
                thresh = offenders[col].mean() * 1.5
                affected_studies = offenders[offenders[col] > thresh].index.tolist()
                if len(affected_studies) >= 3:
                    systemic.append(col)
            insights["Systemic_Risks"] = systemic if systemic else []
        except Exception:
            insights["Systemic_Risks"] = []

        try:
            if insights.get("Worst_Study"):
                pd_col = insights.get("Primary_Driver")
                if pd_col == "SAE_Pending_Count":
                    insights["Bottleneck_Type"] = "Safety-Driven"
                elif pd_col == "Overdue_Visits_Count":
                    insights["Bottleneck_Type"] = "Operational Delay"
                elif pd_col == "Missing_Pages":
                    insights["Bottleneck_Type"] = "Data Entry / Training"
                else:
                    insights["Bottleneck_Type"] = "General Quality"
        except Exception:
            insights["Bottleneck_Type"] = "Unknown"

        return insights
