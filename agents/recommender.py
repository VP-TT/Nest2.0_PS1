def run_recommender(df, root_causes=None):
    recommendations = []

    # If we have root cause signals use them
    if root_causes:

        # DQI decline trend
        trend = root_causes.get("DQI_Trend")
        if trend is not None:
            if trend < -1:
                recommendations.append(
                    "Portfolio DQI declined week-over-week. Deploy cross-study QC taskforce."
                )
            elif trend > 1:
                recommendations.append(
                    "Data quality improving. Continue active monitoring."
                )

        # Worst study driver
        worst_study = root_causes.get("Worst_Study")
        worst_metrics = root_causes.get("Worst_Study_Metrics", {})

        if worst_study:
            if worst_metrics.get("SAE_Pending_Count", 0) > 3:
                recommendations.append(
                    f"{worst_study}: High SAE backlog. Assign medical safety review team."
                )
            if worst_metrics.get("Overdue_Visits_Count", 0) > 2:
                recommendations.append(
                    f"{worst_study}: Overdue visits trending high. Schedule CRA visit blitz."
                )
            if worst_metrics.get("Missing_Pages", 0) > 1:
                recommendations.append(
                    f"{worst_study}: Missing pages indicate site training need."
                )

        # Feature correlation drivers
        corr = root_causes.get("Worst_Correlations", {})
        for col, score in corr.items():
            if abs(score) > 0.4:
                if "SAE" in col:
                    recommendations.append(
                        "SAE burden strongly drags DQI. Trigger SAE-aging escalation workflow."
                    )
                if "Overdue" in col:
                    recommendations.append(
                        "Overdue visits correlate with low DQI. Automate overdue flag reports."
                    )
                if "Missing" in col:
                    recommendations.append(
                        "Missing pages strongly tied to poor DQI. Launch data entry cleanup sprint."
                    )

    # Global study-level rules
    study_means = df.groupby("Study").agg({
        "SAE_Pending_Count": "mean",
        "Overdue_Visits_Count": "mean",
        "Missing_Pages": "mean"
    })

    chronic_bad = study_means[
        (study_means["SAE_Pending_Count"] > 3) &
        (study_means["Overdue_Visits_Count"] > 2)
    ]

    for study in chronic_bad.index:
        recommendations.append(
            f"{study}: Persistent operational drag. Conduct root cause workshop with Site Leads."
        )

    # If no rules triggered (rare)
    if not recommendations:
        recommendations.append("Quality stable across studies — continue routine monitoring.")

    return recommendations
