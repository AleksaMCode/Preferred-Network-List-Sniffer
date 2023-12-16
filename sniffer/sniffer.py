import sys
import threading
from http.client import HTTPException
from parser import parse_ip_packet_wrapper
from pathlib import Path
from time import sleep
from urllib.error import HTTPError

from loguru import logger
from scapy.sendrecv import AsyncSniffer
from websocket import WebSocket, create_connection
from yaspin import yaspin

from settings import CHANNEL_ID, DEFAULT_INTERFACE, LOGGING, MAX_RECONNECT, SERVER

# Create logger.
logger.add(
    f"{Path(__file__).stem}.log",
    format=LOGGING["format"],
    rotation=LOGGING["rotation"],
    retention=LOGGING["retention"],
)

socket_manager: WebSocket = None
trigger = threading.Event()


@yaspin(text="Capturing Probe Requests...")
def capture_traffic(interface: str):
    """
    Captures Wi-Fi traffic and store captured SSIDs.
    """
    sniffer = AsyncSniffer(
        iface=interface,
        prn=parse_ip_packet_wrapper(socket_manager, trigger),
        store=False,
        stop_filter=lambda x: trigger.is_set(),
    )
    sniffer.start()
    sniffer.join()


@yaspin(text="Connecting to the Web Server...")
def connection():
    """
    Attempts to establish socket connection with the server.
    """
    # TODO: Implement a real Backoff Protocol.
    logger.info("Sniffer is trying to open a WebSocket connection to the Web Server.")
    attempt_count = 0
    global socket_manager
    # Try to create connection MAX_RECONNECT times before terminating.
    while True:
        try:
            # Create a socket connection.
            socket_manager = create_connection(
                f"ws://{SERVER['host']}:{SERVER['port']}/ws/pub/{CHANNEL_ID}"
            )
            logger.info("Web socket connection opened.")
            return True
        except Exception as e:
            logger.exception(
                f"There was an error during creation of socket connection: {str(e)}"
            )
            attempt_count += 1
            if attempt_count == MAX_RECONNECT:
                logger.error("Failed to connect to socket after 5 attempts.")
                return False
            logger.info("Trying to reconnect in 30 seconds.")
            sleep(30)


def disconnect():
    if socket_manager and socket_manager.connected:
        socket_manager.close()


if __name__ == "__main__":
    while True:
        if not connection():
            # 126 - Command invoked cannot execute
            sys.exit(126)

        try:
            logger.info("Capture packets from Wi-Fi traffic.")
            capture_traffic(f"{DEFAULT_INTERFACE}mon")
        except (HTTPException, HTTPError) as e:
            logger.exception(f"HTTP Exception: {str(e)}")
        except KeyboardInterrupt as e:
            logger.warning("Sniffer stopped forcefully.")
            disconnect()
            # 130 - Script terminated by Control-C
            sys.exit(130)
        except Exception as e:
            logger.exception(str(e))
        finally:
            logger.info("Sniffer has been stopped.")
            if trigger.is_set():
                # Reset trigger event.
                trigger.clear()
            else:
                disconnect()

        logger.info("Starting the sniffer again.")
