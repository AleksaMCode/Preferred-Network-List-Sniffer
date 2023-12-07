import json
import os
import datetime

CONFIG_FILE = json.load(open(os.path.join(os.path.dirname(__file__), "sniffer.config")))

# Format of the timestamp that will be stored alongside SSID.
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Name of the file that contains Firebase credentials.
FIREBASE_CREDENTIALS = "firebase_credentials.json"

# Timestamp is used to name the main node for storing data.
# Format is 'year + month + day', e.q. 20231202.
FIREBASE_NODE = datetime.datetime.now().strftime("%Y%m%d")

# Logging configuration.
LOGGING = {
    "filename": "pnls.log",
    "format": "[{time}: {level}] {message}",
    "rotation": "30 days",
    "retention": 5,
}
