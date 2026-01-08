import pandas as pd
df = pd.read_csv('outputs/all_studies_noisy.csv')
print(df['SAE_Pending_Count'].describe())
print(df['Overdue_Visits_Count'].describe())
print(df.groupby('Study')['SAE_Pending_Count'].sum().sort_values(ascending=False).head())
