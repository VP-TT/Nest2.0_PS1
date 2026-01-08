import pandas as pd
from datetime import datetime
import os

class AgentBase:
    def __init__(self, name, data_path="outputs/all_studies_noisy.csv", log_dir="logs"):
        self.name = name
        self.data_path = data_path
        self.log_dir = log_dir
        
        # create logs folder if missing
        os.makedirs(log_dir, exist_ok=True)

    def load_data(self):
        """Load latest patient dataset as a DataFrame."""
        return pd.read_csv(self.data_path)

    def log(self, message):
        """Write timestamped entries to a daily log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(self.log_dir, f"{day}.log")
        
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] [{self.name}] {message}\n")

        print(f"[{self.name}] {message}")
