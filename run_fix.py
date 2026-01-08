from agents.monitor import MonitorAgent
from agents.predict import PredictAgent
from agents.alert import AlertAgent
from agents.fix import FixAgent

mon = MonitorAgent()
pred = PredictAgent()
alert = AlertAgent()
fix = FixAgent()

m = mon.run()
p = pred.run()
a = alert.run(m, p)
f = fix.run(m, p)

print(f)
