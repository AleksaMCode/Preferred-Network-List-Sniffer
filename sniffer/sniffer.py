import subprocess
import sys
import threading
from http.client import HTTPException
from parser import parse_ip_packet_wrapper
from pathlib import Path
from urllib.error import HTTPError

from scapy.sendrecv import AsyncSniffer
from websocket import WebSocketApp
from yaspin import yaspin

from logger import create_logger, log_exception, log_info, log_warning
from settings import DEFAULT_INTERFACE
from socket_manager import connect, disconnect, trigger

# Create a logger.
create_logger(f"{Path(__file__).stem}.log")


@yaspin(text="Capturing Probe Requests...")
def capture_traffic(web_socket: WebSocketApp, web_socket_thread: threading.Thread):
    """
    Captures Wi-Fi traffic and publish SSIDs and other information.
    """
    sniffer = AsyncSniffer(
        iface=f"{DEFAULT_INTERFACE}mon",
        prn=parse_ip_packet_wrapper(web_socket, trigger),
        store=False,
        stop_filter=lambda x: trigger.is_set(),
    )
    sniffer.start()
    sniffer.join()
    web_socket_thread.join()


@yaspin(text="Checking interface mode...")
def check_inteface_mode():
    """
    Checks if the wireless interface has been set to the Monitor mode.
    """
    interface_info = subprocess.run(
        ["iwconfig", f"{DEFAULT_INTERFACE}mon"], capture_output=True, text=True
    ).stdout
    try:
        # Parse out only the interface mode.
        interface_mode = interface_info.split("Mode:", 1)[1].split(" ", 1)[0]

        if interface_mode == "Monitor":
            return True
    except:
        return False

    return False


def start():
    if not check_inteface_mode():
        log_info(f"Failed to start the sniffer due to missing monitor interface.")
        # 126 - Command invoked cannot execute
        sys.exit(126)

    while True:
        # Create a socket connection to server.
        web_socket, web_socket_thread = connect()
        if not web_socket:
            sys.exit(126)

        try:
            log_info("Capture packets from Wi-Fi traffic.")
            # Capture the Wi-Fi packets.
            capture_traffic(web_socket, web_socket_thread)
        except (HTTPException, HTTPError) as e:
            log_exception(f"HTTP Exception: {str(e)}")
        except KeyboardInterrupt as e:
            log_warning("Sniffer stopped forcefully.")
            disconnect(web_socket)
            # 130 - Script terminated by Control-C
            sys.exit(130)
        except Exception as e:
            log_exception(str(e))
        finally:
            log_info("Sniffer has been stopped.")
            if trigger.is_set():
                # Reset trigger event.
                trigger.clear()
            disconnect(web_socket)

        log_info("Starting the sniffer again.")


if __name__ == "__main__":
    start()
