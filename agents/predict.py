import numpy as np

class PredictAgent:
    def __init__(self, df, model, features, name="PredictAgent"):
        self.df = df
        self.model = model
        self.features = features
        self.name = name

    def run(self):
        df = self.df.copy()

        for c in self.features:
            if c not in df.columns:
                df[c] = 0

        X = df[self.features]
        probs = self.model.predict_proba(X)[:, 1]
        df["Future_HighRisk_Probability"] = (probs * 100).round(1)

        very_high = int((df["Future_HighRisk_Probability"] >= 70).sum())
        at_risk = int((df["Future_HighRisk_Probability"] >= 40).sum())
        avg_prob = float(df["Future_HighRisk_Probability"].mean())

        return {
            "Avg_Prob": round(avg_prob, 2),
            "VeryHigh_Count": very_high,
            "AtRisk_Count": at_risk,
            "Top_5": df.nlargest(5, "Future_HighRisk_Probability")[[
                "Subject ID", "Study", "Future_HighRisk_Probability"
            ]].to_dict(orient="records")
        }
