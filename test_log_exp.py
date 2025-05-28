from src.custon_exception import CustomException
from src.logger import get_logger
import sys

logger = get_logger(__name__) 

def divide_number(a, b):
    try:
        result = a/b
        logger.info("Numbers divided successfully")
        return result
    except Exception as e:
        logger.error("Error occurred while dividing numbers") 
        raise CustomException("Custom error zero", sys)
    
if __name__ == "__main__":
    try:
        logger.info("Starting the division process")
        divide_number(10, 0)
    except CustomException as ce:
        logger.error(str(ce)) 