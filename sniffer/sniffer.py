from scapy.sendrecv import AsyncSniffer
from parser import parse_ip_packet_wrapper
from websocket.websocket_manager import WebSocketManager


def capture_traffic(interface: str, socket_manager: WebSocketManager):
    """
    Capture Wi-Fi traffic and store captured SSIDs.
    """
    sniffer = AsyncSniffer(iface=interface, prn=parse_ip_packet_wrapper(socket_manager))
    sniffer.start()
    sniffer.join()
