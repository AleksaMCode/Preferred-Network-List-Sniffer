import firebase_admin
from firebase_admin import db, credentials

from datetime import datetime
from scapy.layers.dot11 import Dot11ProbeReq

from settings import CONFIG_FILE, FIREBASE_CREDENTIALS, FIREBASE_NODE
from settings import TIMESTAMP_FORMAT

firebase_admin.initialize_app(
    credentials.Certificate(FIREBASE_CREDENTIALS),
    {list(CONFIG_FILE.keys())[0]: CONFIG_FILE[list(CONFIG_FILE.keys())[0]]},
)


def parse_ip_packet(packet):
    """
    Filters the packet and upload sniffer data (SSID + timestamp) to a Firebase database using `update` function.
    """
    # Filter only Probe Request and ignore Probe Requests with wildcard in the SSID field.
    if packet.haslayer(Dot11ProbeReq):
        ssid = packet.info.decode("utf-8")
        if ssid:
            db.reference(f"/{FIREBASE_NODE}").update(
                {
                    ssid: datetime.utcfromtimestamp(float(packet.time)).strftime(
                        TIMESTAMP_FORMAT
                    )
                }
            )
