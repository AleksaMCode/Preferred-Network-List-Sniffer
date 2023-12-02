import sys
import threading

from sniffer import clear_old_traffic, capture_traffic

clear_old_traffic()

t1 = threading.Thread(target=capture_traffic(f"{sys.argv[1]}mon"), args=[])
t1.start()
