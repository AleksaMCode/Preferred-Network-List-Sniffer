import firebase_admin
from firebase_admin import db, credentials
from yaspin import yaspin

from parser import parse_traffic_file
from settings import CONFIG_FILE, FIREBASE_CREDENTIALS

# Create a new app instance using the credentials and database name.
firebase_admin.initialize_app(
    credentials.Certificate(FIREBASE_CREDENTIALS),
    {list(CONFIG_FILE.keys())[0]: CONFIG_FILE[list(CONFIG_FILE.keys())[0]]},
)


def upload_to_firebase(node):
    """
    Upload sniffed data (SSID + timestamp) to a Firebase database using `update` function.
    """
    data = parse_traffic_file()
    if data:
        spinner = yaspin(text="Uploading data to database...")
        spinner.start()
        db.reference(f"/{node}").update(data)
        spinner.stop()
