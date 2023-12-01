import subprocess
from datetime import time


def sniff(interface):
    timeout = 60 * 3
    start_time = time.time()

    airodump = subprocess.Popen(['airodump-ng', interface], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)

    while time.time() < start_time + timeout:
        print(airodump.stdout.readline())

    airodump.terminate()


sniff("wlan0mon")