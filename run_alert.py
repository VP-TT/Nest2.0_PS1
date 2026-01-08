from agents.monitor import MonitorAgent
from agents.predict import PredictAgent
from agents.alert import AlertAgent

mon = MonitorAgent()
pred = PredictAgent()
alert = AlertAgent()

monitor_output = mon.run()
predict_output = pred.run()

result = alert.run(monitor_output, predict_output)
print(result)
