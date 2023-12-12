import json

from datetime import datetime
from scapy.layers.dot11 import Dot11ProbeReq

from settings import CHANNEL_ID
from settings import TIMESTAMP_FORMAT


def parse_ip_packet_wrapper(socket_manager):
    def parse_ip_packet(packet):
        """
        Filters the packet and broadcasts sniffed data (SSID + timestamp) to a Redis channel.
        """
        # Filter only Probe Request and ignore Probe Requests with wildcard in the SSID field.
        if packet.haslayer(Dot11ProbeReq):
            ssid = packet.info.decode("utf-8")
            if ssid:
                # await
                socket_manager.broadcast_to_room(CHANNEL_ID, json.dumps({
                    ssid: datetime.utcfromtimestamp(float(packet.time)).strftime(
                        TIMESTAMP_FORMAT
                    )
                }))
