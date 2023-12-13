import datetime

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
