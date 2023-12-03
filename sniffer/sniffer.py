import os
import re
import subprocess
import time

TRAFFIC_FILE = "traffic"


def clear_old_traffic():
    """
    Removes old traffic files
    """
    for file in os.listdir(os.path.dirname(__file__)):
        if re.match(f"{TRAFFIC_FILE}.*\.cap", file):
            os.remove(file)


def capture_traffic(interface):
    """
    Capture Wi-Fi traffic using airodump-ng and store data in a cap file.
    """
    total_time = 30
    start_time = time.time()

    handle = subprocess.Popen(
        [
            "sudo",
            "airodump-ng",
            "-w",
            os.path.join(os.path.dirname(__file__), TRAFFIC_FILE),
            "--output-format",
            "cap",
            interface,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    while time.time() < start_time + total_time:
        pass

    handle.terminate()
    handle.wait()
