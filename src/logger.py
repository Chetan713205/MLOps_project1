import logging
import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok = True)            # Create logs directory if it doesn't exist

# Day by day log file creation
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log") 

logging.basicConfig(
    filename = LOG_FILE,
    format = "[%(asctime)s] %(levelname)s - %(message)s",
    level = logging.INFO                                        # Out of several only INFO, WARNING, ERROR will be shown
)

def get_logger(name):
    logger = logging.getLogger(name)                        # Create a logger object
    logger.setLevel(logging.INFO)                           # Set the logging level
    return logger 