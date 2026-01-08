from agents.fix_action import FixActionAgent

fake_ctx = {
    "monitor": {
        "Sites": [
            {"Site_ID": 101, "HighRisk_Patients": 23, "SAE_Pending": 15, "Overdue_Visits": 10},
            {"Site_ID": 220, "HighRisk_Patients": 11, "SAE_Pending": 7, "Overdue_Visits": 4},
            {"Site_ID": 305, "HighRisk_Patients": 4, "SAE_Pending": 1, "Overdue_Visits": 0}
        ]
    }
}

print(FixActionAgent().run(fake_ctx))
