import json
import os

CONFIG_FILE = json.load(open(os.path.join(os.path.dirname(__file__), "sniffer.config")))

# Format of the timestamp that will be stored alongside SSID.
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Name of the files that contain sniffed Wi-Fi traffic.
TRAFFIC_FILE = "traffic"

# Name of the file that contains Firebase credentials.
FIREBASE_CREDENTIALS = "firebase_credentials.json"

# Logging configuration.
LOGGING = {
    "filename": "pnls.log",
    "format": "[{time}: {level}] {message}",
    "rotation": "30 days",
    "retention": 5,
}
