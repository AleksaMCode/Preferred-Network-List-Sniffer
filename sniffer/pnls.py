import sys
import threading

from db_client import send_data
from sniffer import clear_old_traffic, capture_traffic

clear_old_traffic()

t1 = threading.Thread(target=capture_traffic(f"{sys.argv[1]}mon"), args=[])
t2 = threading.Thread(target=send_data(), args=[])
t1.start()
t2.start()
