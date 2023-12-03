import datetime
import sys
from db_client import upload_to_firebase
from sniffer import clear_old_traffic, capture_traffic

if __name__ == "__main__":
    # Timestamp is used to name the main node for storing data. The format is 'year + month + day', e.q. 20231202.
    timestamp = datetime.datetime.now().strftime("%Y%m%d")

    while True:
        clear_old_traffic()
        capture_traffic(f"{sys.argv[1]}mon")
        upload_to_firebase(timestamp)
