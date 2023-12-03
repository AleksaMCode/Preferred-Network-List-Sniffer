import unittest
import datetime

import firebase_admin
from firebase_admin import db, credentials

from db_client import upload_to_firebase
from parser import parse_traffic_file


class TestDbClient(unittest.TestCase):
    input_data = parse_traffic_file()

    @classmethod
    def setUpClass(cls) -> None:
        cls.node = f"{datetime.datetime.now().strftime('%Y%m%d')}-test"
        cred = credentials.Certificate("firebase_credentials.json")
        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": "https://pnl-sniffer-default-rtdb.europe-west1.firebasedatabase.app/"
            },
        )

    @classmethod
    def tearDownClass(cls):
        db.reference(f"/{cls.node}").delete()

    def test_upload(self):
        upload_to_firebase(self.node)
        output_data = db.reference(f"/{self.node}").get()
        self.assertDictEqual(output_data, self.input_data)
