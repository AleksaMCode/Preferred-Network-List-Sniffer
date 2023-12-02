import os
import re
import subprocess
import sys

TRAFFIC_FILE = "traffic"


def clear_old_traffic():
    """
    Removes old traffic files
    """
    for file in os.listdir("."):
        if re.match(f"{TRAFFIC_FILE}.*\.cap", file):
            os.remove(file)


def capture_traffic(interface):
    """
    Capture Wi-Fi traffic using airodump-ng and store data in a cap file.
    """
    subprocess.run(
        ["airodump-ng", "-w", TRAFFIC_FILE, "--output-format", "cap", interface],
        capture_output=True,
    )


clear_old_traffic()
# TODO: Run sniffing on a new thread.
capture_traffic(f"{sys.argv[1]}mon")    
