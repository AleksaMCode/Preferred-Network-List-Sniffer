import json
import sys
import threading
from datetime import datetime

from websocket import WebSocketApp

from settings import TIMESTAMP_FORMAT
from socket_manager import connect, disconnect


def generate_data(web_socket: WebSocketApp, web_socket_thread: threading.Thread):
    count = 1
    while True:
        web_socket.send(
            json.dumps(
                {
                    "ssid": f"ssid_{count}",
                    "timestamp": datetime.strptime(str(datetime.now()), TIMESTAMP_FORMAT)
                }
            )
        )
        count += 1


def start():
    # Create a socket connection to server.
    web_socket, web_socket_thread = connect()
    if not web_socket:
        # 126 - Command invoked cannot execute
        sys.exit(126)

    try:
        # Generate fake SSIDs with timestamps.
        generate_data(web_socket, web_socket_thread)
    except KeyboardInterrupt:
        disconnect(web_socket)
        # 130 - Script terminated by Control-C
        sys.exit(130)
    except Exception:
        pass
    finally:
        disconnect(web_socket)


if __name__ == "__main__":
    start()
