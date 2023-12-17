import datetime

# Name of the interface that will be used for monitoring mode.
DEFAULT_INTERFACE = "wlan0"

# Server configuration.
SERVER = {
    # localhost address is needed when using `uvicorn` to start the server
    # in order to make it visible on the local network.
    "localhost": "0.0.0.0",
    "host": "127.0.0.1",
    "port": 3_001,
    "redis_host": "127.0.0.1",
    "redis_port": 6_379,
}

# Number of maximum reconnect attempts to the server before terminating sniffer.
MAX_RECONNECT = 5

# Time delay, in seconds, between sniffer reconnect attempts.
DELAY = 30

# Format of the timestamp that will be stored alongside SSID.
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Timestamp is used to name the channel id for storing data.
# Format is 'year + month + day', e.q. 20231202.
CHANNEL_ID = datetime.datetime.now().strftime("%Y%m%d")

# Logging configuration.
LOGGING = {
    "format": "[{time}: {level}] {message}",
    "rotation": "30 days",
    "retention": 5,
}
