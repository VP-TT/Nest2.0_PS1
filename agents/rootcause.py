import pandas as pd

class RootCauseAgent:
    def __init__(self, df, prev_df=None, name="RootCauseAgent"):
        self.df = df
        self.prev_df = prev_df
        self.name = name

    def run(self):
        df = self.df
        prev_df = self.prev_df
        insights = {}

        try:
            numeric = df.select_dtypes(include='number')
            corr = numeric.corr()['Smart_DQI_Noisy'].sort_values()
            worst_corr = corr.head(3)
            insights["Worst_Correlations"] = {
                col: round(val, 3) for col, val in worst_corr.items()
            }
        except Exception:
            insights["Worst_Correlations"] = {}

        try:
            study_agg = df.groupby("Study").agg({
                'Smart_DQI_Noisy': 'mean',
                'SAE_Pending_Count': 'mean',
                'Overdue_Visits_Count': 'mean',
                'Missing_Pages': 'mean'
            }).sort_values('Smart_DQI_Noisy')

            worst_study = study_agg.index[0]
            insights["Worst_Study"] = worst_study
            insights["Worst_Study_Metrics"] = study_agg.loc[worst_study].round(2).to_dict()

            best_study = study_agg.index[-1]
            deltas = (study_agg.loc[worst_study] - study_agg.loc[best_study]).round(2)
            insights["Gap_Between_Best_And_Worst"] = deltas.to_dict()
        except Exception:
            pass

        if isinstance(prev_df, pd.DataFrame):
            try:
                prev_avg = prev_df['Smart_DQI_Noisy'].mean()
                curr_avg = df['Smart_DQI_Noisy'].mean()
                insights["DQI_Trend"] = round(curr_avg - prev_avg, 2)
            except Exception:
                insights["DQI_Trend"] = None

        return insights
