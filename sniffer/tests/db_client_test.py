import unittest
import datetime

from firebase_admin import db

from db_client import upload_to_firebase
from parser import parse_traffic_file


class TestDbClient(unittest.TestCase):
    input_data = parse_traffic_file()

    @classmethod
    def setUpClass(cls) -> None:
        cls.node = f"{datetime.datetime.now().strftime('%Y%m%d')}-test"

    @classmethod
    def tearDownClass(cls):
        db.reference(f"/{cls.node}").delete()

    def test_upload(self):
        upload_to_firebase(self.node)
        output_data = db.reference(f"/{self.node}").get()
        self.assertDictEqual(output_data, self.input_data)
