import os
import requests

class FixActionAgent:
    def __init__(self, name="FixActionAgent"):
        self.name = name
        self.slack = os.getenv("SLACK_WEBHOOK")

    def build_sites(self, df):
        grouped = df.groupby("Site ID").agg({
            "Smart_Risk_Noisy": lambda x: (x == "High").sum(),
            "SAE_Pending_Count": "sum",
            "Overdue_Visits_Count": "sum"
        }).reset_index()

        sites = []
        for _, row in grouped.iterrows():
            sites.append({
                "Site_ID": row["Site ID"],
                "HighRisk_Patients": int(row["Smart_Risk_Noisy"]),
                "SAE_Pending": int(row["SAE_Pending_Count"]),
                "Overdue_Visits": int(row["Overdue_Visits_Count"])
            })
        return sites

    def rank_sites(self, sites):
        return sorted(
            sites,
            key=lambda s: (
                -s["HighRisk_Patients"],
                -s["SAE_Pending"],
                -s["Overdue_Visits"]
            )
        )

    def allocate_cras(self, ranked_sites, cras_available=3):
        plan = []
        for idx, site in enumerate(ranked_sites):
            if idx < cras_available:
                plan.append({
                    "Site": site["Site_ID"],
                    "Assigned CRA": f"CRA-{idx+1}",
                    "Reason": f"{site['HighRisk_Patients']} high-risk, {site['SAE_Pending']} SAE"
                })
        return plan

    def write_plan(self, ranked_sites, assignments):
        msg = "📋 *Autonomous Action Plan Generated*\n\n"
        msg += "🏥 *Critical Sites Ranked:*\n"
        for s in ranked_sites[:5]:
            msg += f"• Site {s['Site_ID']} → {s['HighRisk_Patients']} high-risk | {s['SAE_Pending']} SAE | {s['Overdue_Visits']} overdue\n"
        msg += "\n👷 *CRA Allocation:*\n"
        for a in assignments:
            msg += f"• {a['Assigned CRA']} → Site {a['Site']} ({a['Reason']})\n"
        return msg

    def notify(self, text):
        if not self.slack:
            return "slack_skipped"
        resp = requests.post(self.slack, json={"text": text})
        return "slack_sent" if resp.status_code == 200 else f"slack_error:{resp.status_code}"

    def run(self, ctx):
        df = ctx["predict"].get("df_source", None)
        if df is None:
            df = ctx["df"] if "df" in ctx else None
        if df is None:
            return {"status": "no_data"}

        sites = self.build_sites(df)
        ranked_sites = self.rank_sites(sites)
        assignments = self.allocate_cras(ranked_sites)
        plan = self.write_plan(ranked_sites, assignments)
        notify_status = self.notify(plan)

        return {
            "sites_ranked": ranked_sites[:5],
            "assignments": assignments,
            "notify": notify_status
        }
