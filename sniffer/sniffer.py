from scapy.sendrecv import AsyncSniffer
from parser import parse_ip_packet_wrapper


def capture_traffic(interface, socket_manager):
    """
    Capture Wi-Fi traffic and store captured SSIDs.
    """
    sniffer = AsyncSniffer(iface=interface, prn=parse_ip_packet_wrapper(socket_manager))
    sniffer.start()
    sniffer.join()
