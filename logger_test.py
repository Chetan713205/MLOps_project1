from src.logger import get_logger

logger = get_logger(__name__)                               # __name__ is a special variable in Python that holds the name of the current module
logger.info("Logging has been set up.")                   # Log an info message