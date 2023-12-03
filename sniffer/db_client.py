import datetime
import json
import os

import firebase_admin
from firebase_admin import db, credentials

from parser import parse_traffic_file

CONFIG_FILE_NAME = "sniffer.config"
CONFIG_FILE = json.load(open(os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)))


def upload_to_firebase(node):
    """
    Upload sniffed data to firebase database using `update` function.
    """
    data = parse_traffic_file()
    if data:
        db.reference(f"/{node}").update(data)


def send_data():
    """
    Sends sniffed data (SSID + timestamp) to a Firebase database.
    """
    # Get databaseUrl key from config file.
    database_url = list(CONFIG_FILE.keys())[0]

    # Load Firebase credentials.
    cred = credentials.Certificate("firebase_credentials.json")

    # Create a new app instance using the loaded credentials and database name.
    firebase_admin.initialize_app(cred, {database_url: CONFIG_FILE[database_url]})

    # Timestamp is used to name the main node for storing data. The format is 'year + month + day', e.q. 20231202.
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    upload_to_firebase(timestamp)
