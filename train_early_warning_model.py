import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load data
df = pd.read_csv("outputs/all_studies_noisy.csv")

# Target: will patient become High Risk
df["TargetHigh"] = (df["Smart_Risk_Noisy"] == "High").astype(int)

# Feature engineering
df["Total_Issues"] = (
    df["SAE_Pending_Count"]
    + df["Overdue_Visits_Count"]
    + df["Missing_Pages"]
)

feature_cols = [
    "Smart_DQI_Noisy",
    "SAE_Pending_Count",
    "Overdue_Visits_Count",
    "Missing_Pages",
    "Total_Issues"
]

X = df[feature_cols]
y = df["TargetHigh"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Model
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Save
joblib.dump(
    {
        "model": model,
        "features": feature_cols
    },
    "early_warning_model.pkl"
)

print("✅ Early warning model trained & saved")
