# For reading .yaml files 
import os
from src.logger import get_logger 
from src.custom_exception import CustomException
import pandas as pd
import yaml
import sys 

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise CustomException(f"YAML file not found at path: {file_path}", sys)
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Sucessfully read the .yaml file")
        return config
    except Exception as e:
        logger.error("Error occured during reading of .yaml file")
        raise CustomException(f"Error reading YAML file: {e}", sys) 
    
def load_data(path):
    try:
        logger.info(f"Loading data from {path}")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading data from {path}: {e}")
        raise CustomException(f"Error loading data: {e}", sys)