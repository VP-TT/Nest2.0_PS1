from agents.monitor import MonitorAgent
from agents.predict import PredictAgent
from agents.alert import AlertAgent
from agents.fix import FixAgent
from agents.report import ReportAgent

mon = MonitorAgent()
pred = PredictAgent()
alert = AlertAgent()
fix = FixAgent()
report = ReportAgent()

m = mon.run()
p = pred.run()
a = alert.run(m, p)
f = fix.run(m, p)
r = report.run(m, p, a, f)

print(r)
