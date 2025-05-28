import os
import sys
import pandas as pd
from google.cloud import storage 
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import RAW_FILE_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH, CONFIG_PATH, RAW_DIR # Or simply import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]
        
        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data ingestion started with bucket: {self.bucket_name} and file: {self.bucket_file_name}")  
        
    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"File downloaded from GCP bucket: {self.bucket_name} to local path: {RAW_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error downloading file from GCP: {e}")
            raise CustomException(f"Error downloading file from GCP: {e}", sys)
        
    def split_data(self):
        try:
            df = pd.read_csv(RAW_FILE_PATH)
            logger.info(f"Data loaded from {RAW_FILE_PATH} with shape: {df.shape}")
            
            train_df, test_df = train_test_split(df, test_size=1-self.train_test_ratio, random_state=42)
            logger.info(f"Data split into train and test sets with shapes: {train_df.shape}, {test_df.shape}")
            
            train_df.to_csv(TRAIN_FILE_PATH, index=False)
            test_df.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f"Train data saved to {TRAIN_FILE_PATH} and test data saved to {TEST_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error during data splitting: {e}")
            raise CustomException(f"Error during data splitting: {e}", sys)
        
    def run(self):
        try:
            logger.info(f"Starting data ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info(f"Data ingestion process completed successfully")
        except Exception as e:
            logger.error(f"Error in data ingestion process: {e}")
            raise CustomException(f"Error in data ingestion process: {e}", sys) 
        finally:
            logger.info(f"Data ingestion process finished")

# Whaever you write under this script will automatically execute as soon as you run python data_ingestion.py            
if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
