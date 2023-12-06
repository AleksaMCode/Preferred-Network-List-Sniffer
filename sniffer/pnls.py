import sys
from http.client import HTTPException
from urllib.error import HTTPError

from settings import LOGGING
from sniffer import capture_traffic
from loguru import logger

logger.add(
    LOGGING["filename"],
    format=LOGGING["format"],
    rotation=LOGGING["rotation"],
    retention=LOGGING["rotation"],
)

if __name__ == "__main__":
    while True:
        try:
            logger.info("Clear Wi-Fi traffic files.")
            clear_old_traffic()
            logger.info("Capture packages from Wi-Fi traffic.")
            capture_traffic(f"{sys.argv[1]}mon")
            logger.info("Upload PNL data to Firebase.")
            upload_to_firebase(timestamp)
        except (HTTPException, HTTPError) as e:
            logger.exception(f"HTTP Exception: {str(e)}")
        except KeyboardInterrupt as e:
            logger.warning("Sniffer stopped forcefully.")
            sys.exit(130)
        except Exception as e:
            logger.exception(str(e))
