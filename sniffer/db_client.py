import json
import os

import firebase_admin
from firebase_admin import db, credentials

from parser import parse_traffic_file

CONFIG_FILE = json.load(open(os.path.join(os.path.dirname(__file__), "sniffer.config")))

# Create a new app instance using the credentials and database name.
firebase_admin.initialize_app(
    credentials.Certificate("firebase_credentials.json"),
    {list(CONFIG_FILE.keys())[0]: CONFIG_FILE[list(CONFIG_FILE.keys())[0]]},
)


def upload_to_firebase(node):
    """
    Upload sniffed data (SSID + timestamp) to a Firebase database using `update` function.
    """
    data = parse_traffic_file()
    if data:
        db.reference(f"/{node}").update(data)
