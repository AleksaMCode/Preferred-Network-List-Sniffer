import datetime
import sys
from http.client import HTTPException

from db_client import upload_to_firebase
from sniffer import clear_old_traffic, capture_traffic
from loguru import logger

logger.add(
    "pnls.log",
    format="[{time}: {level}] {message}]",
    rotation="30 days",
    retention=5,
)

if __name__ == "__main__":
    # Timestamp is used to name the main node for storing data. The format is 'year + month + day', e.q. 20231202.
    timestamp = datetime.datetime.now().strftime("%Y%m%d")

    while True:
        try:
            logger.info("Clear old Wi-Fi traffic files.")
            clear_old_traffic()
            logger.info("Capture PNL from Wi-Fi traffic.")
            capture_traffic(f"{sys.argv[1]}mon")
            logger.info("Upload PNL data to Firebase.")
            upload_to_firebase(timestamp)
        except HTTPException as e:
            logger.exception(f"HTTP Exception: {str(e)}")
        except KeyboardInterrupt as e:
            logger.warning(f"Sniffer stopped forcefully: {str(e)}")
            sys.exit(130)
        except Exception as e:
            logger.exception(str(e))
