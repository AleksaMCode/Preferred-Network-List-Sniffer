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
            logger.info("Capture packages from Wi-Fi traffic.")
            capture_traffic(f"{sys.argv[1]}mon")
        except (HTTPException, HTTPError) as e:
            logger.exception(f"HTTP Exception: {str(e)}")
        except KeyboardInterrupt as e:
            logger.warning("Sniffer stopped forcefully.")
            sys.exit(130)
        except Exception as e:
            logger.exception(str(e))
