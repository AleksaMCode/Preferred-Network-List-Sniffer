import json
import os

CONFIG_FILE = json.load(open(os.path.join(os.path.dirname(__file__), "sniffer.config")))

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
TRAFFIC_FILE = "traffic"
FIREBASE_CREDENTIALS = "firebase_credentials.json"
