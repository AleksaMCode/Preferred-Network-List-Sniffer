import sys
from http.client import HTTPException

from logger import create_logger
from parser import parse_ip_packet_wrapper
from pathlib import Path
from urllib.error import HTTPError

from loguru import logger
from scapy.sendrecv import AsyncSniffer
from yaspin import yaspin

from settings import DEFAULT_INTERFACE

from socket_manager import connect, disconnect, web_socket, trigger

create_logger(f"{Path(__file__).stem}.log")


@yaspin(text="Capturing Probe Requests...")
def capture_traffic(interface: str):
    """
    Captures Wi-Fi traffic and store captured SSIDs.
    """
    sniffer = AsyncSniffer(
        iface=interface,
        prn=parse_ip_packet_wrapper(web_socket, trigger),
        store=False,
        stop_filter=lambda x: trigger.is_set(),
    )
    sniffer.start()
    sniffer.join()


if __name__ == "__main__":
    while True:
        if not connect():
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
