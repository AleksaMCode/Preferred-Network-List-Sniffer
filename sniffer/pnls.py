import sys
import threading
import time
from db_client import send_data
from sniffer import clear_old_traffic, capture_traffic

while True:
    clear_old_traffic()
    capture_traffic(f"{sys.argv[1]}mon")
    send_data()
