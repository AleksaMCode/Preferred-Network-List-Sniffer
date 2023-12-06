import os
import re
import subprocess
import time

from settings import CONFIG_FILE, TRAFFIC_FILE


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
    total_time = CONFIG_FILE["total_sniffing_time"]
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

    # Wait `total_time` sec. before terminating.
    while time.time() < start_time + total_time:
        pass

    handle.terminate()
    handle.wait()
