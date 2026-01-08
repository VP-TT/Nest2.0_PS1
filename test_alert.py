from agents.alert import AlertAgent

fake_ctx = {
    "monitor": {
        "High_Risk_Pct": 25,
        "SAE_Pending_Total": 300,
        "Critical_Site_Count": 4
    }
}

result = AlertAgent().run(fake_ctx)
print(result)
