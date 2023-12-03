import os
from typing import Dict

import pyshark
from datetime import datetime

from sniffer import TRAFFIC_FILE


def parse_traffic_file() -> Dict[str, str]:
    """
    Parse *.cap file in order to get SSIDs from device's Preferred Network List.
    :return: Dictionary with SSID-timestamp pairs.
    """
    ssids = {}
    # airodump-ng names output with an automatic numbers, where the first file contains '-01'.
    filename = os.path.join(os.path.dirname(__file__), f"{TRAFFIC_FILE}-01.cap")
    capture = pyshark.FileCapture(filename)

    # TODO: Optimize by implementing skipping already read packages.
    for package in capture:
        # Filter only Probe Request and ignore Probe Requests with wildcard in the SSID field.
        if int(package["wlan"].fc, 16) == 16384:
            ssid = package["wlan.mgt"].wlan_tag.split(":")[2].strip().strip('"')
            if "Wildcard" not in ssid:
                ssids[ssid] = datetime.utcfromtimestamp(
                    float(package.sniff_timestamp)
                ).strftime("%Y-%m-%d %H:%M:%S")
    return ssids
