from scapy.all import sniff
from parser import parse_ip_packet
from yaspin import yaspin


@yaspin(text="Capturing SSIDs...")
def capture_traffic(interface):
    """
    Capture Wi-Fi traffic and store captured SSIDs.
    """
    sniff(iface=interface, prn=parse_ip_packet)
