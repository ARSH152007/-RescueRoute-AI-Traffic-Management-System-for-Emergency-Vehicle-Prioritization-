import csv
import os
from datetime import datetime

FILE_NAME = "traffic_data.csv"

def log_data(edge_count):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)

        # Header (only first time)
        if not file_exists:
            writer.writerow(["time", "edge", "vehicle_count"])

        current_time = datetime.now().strftime("%H:%M:%S")

        for edge, count in edge_count.items():
            writer.writerow([current_time, edge, count])