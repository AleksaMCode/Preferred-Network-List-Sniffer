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


def sniff(interface):
    subprocess.run(
        ["airodump-ng", "-w", TRAFFIC_FILE, "--output-format", "cap", interface],
        capture_output=True,
    )


clear_old_traffic()
# TODO: Run sniffing on new thread.
sniff(f"{sys.argv[1]}mon")
