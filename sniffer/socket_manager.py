import threading
from time import sleep

from websocket import WebSocketApp
from yaspin import yaspin

from logger import log_error, log_exception, log_info
from settings import CHANNEL_ID, MAX_RECONNECT, SERVER

trigger = threading.Event()


def on_error(ws, error):
    log_error(f"There was an error during the socket connection: {error}")
    trigger.set()


def on_close(ws, close_status_code, close_msg):
    log_info(
        f"Web socket connection closed with code {close_status_code}: {close_msg}"
    )
    trigger.set()


def on_open(ws):
    log_info("Web socket connection opened.")


@yaspin(text="Connecting to the Web Server...")
def connect():
    """
    Attempts to establish socket connection with the server.
    """
    # TODO: Implement a real Backoff Protocol.
    log_info("Sniffer is trying to open a WebSocket connection to the Web Server.")
    if trigger.is_set():  # Reset trigger event.
        trigger.clear()
    attempt_count = 0
    # Try to create connection MAX_RECONNECT times before terminating.
    while True:
        try:
            # Create a socket connection.
            web_socket = WebSocketApp(
                f"ws://{SERVER['host']}:{SERVER['port']}/ws/pub/{CHANNEL_ID}",
                on_open=on_open,
                on_error=on_error,
                on_close=on_close,
            )
            # Set dispatcher to automatic reconnection, 5 seconds reconnect delay if connection closed unexpectedly
            web_socket_thread = threading.Thread(
                target=web_socket.run_forever, daemon=False
            )
            web_socket_thread.start()
            # Socket connection isn't instant which is why the delay of 1 sec. is added.
            sleep(1)
            if web_socket.sock and web_socket.sock.connected:
                return web_socket, web_socket_thread
        except Exception as e:
            log_exception(
                f"There was an error during creation of socket connection: {str(e)}"
            )
        attempt_count += 1
        if attempt_count == MAX_RECONNECT:
            log_error("Failed to connect to socket after 5 attempts.")
            return None
        log_info("Trying to reconnect in 30 seconds.")
        sleep(30)


def disconnect(web_socket):
    web_socket.close()
