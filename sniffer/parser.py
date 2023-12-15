import json
from datetime import datetime

from scapy.layers.dot11 import Dot11ProbeReq
from websocket import WebSocket

from settings import TIMESTAMP_FORMAT


def parse_ip_packet_wrapper(socket_manager: WebSocket):
    def parse_ip_packet(packet):
        """
        Filters the packet and broadcasts sniffed data (SSID + timestamp) through a websocket.
        """
        # Filter only Probe Request and ignore Probe Requests with wildcard in the SSID field.
        if packet.haslayer(Dot11ProbeReq):
            ssid = packet.info.decode("utf-8")
            if ssid:
                socket_manager.send(
                    json.dumps(
                        {
                            "ssid": ssid,
                            "timestamp": datetime.utcfromtimestamp(
                                float(packet.time)
                            ).strftime(TIMESTAMP_FORMAT),
                        }
                    )
                )

    return parse_ip_packet
