import os
import sys
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)
        
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger.info(f"Created directory: {self.processed_dir}")
            
    def preprocessed_data(self, df):
        try:
            logger.info("Starting data preprocessing")
            logger.info("Dropping the unnecessary columns and deleting duplicates")
            df.drop(columns = ["Booking_ID"], inplace = True)
            df.drop_duplicates(inplace = True)
            
            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"] 
            
            logger.info(f"Applying Label Encoding to categorical features: {cat_cols}")
            label_encoder = LabelEncoder()
            mappings = {}
            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
            logger.info(f"Label Encoding mappings are:")
            for key, value in mappings.items():
                logger.info(f"{key} : {value}")
                
            logger.info("Handling Skewness")
            skewness_threshold =self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew())
            for col in skewness[skewness > skewness_threshold].index:
                df[col] = np.log1p(df[col])
            return df 
        except Exception as e:
            logger.error(f"Error in preprocessing data: {e}")
            raise CustomException(e, sys)
        
    def balance_data(self, df):
        try:
            logger.info("Balancing the data using SMOTE")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']
            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)
            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled
            logger.info("Data balancing completed")
            return balanced_df
        except Exception as e:
            logger.error(f"Error in balancing data: {e}")
            raise CustomException(e, sys) 
        
    def select_features(self, balanced_df):
        try:
            logger.info("Selecting features using Random Forest")
            X = balanced_df.drop(columns=['booking_status'])
            y = balanced_df['booking_status']
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X, y)
            Feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'Feature': X.columns,
                'Importance': Feature_importance
            })
            top_feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
            num_features_to_select = self.config["data_processing"]["no_of_features"] 
            top_10_features = top_feature_importance_df["Feature"].head(num_features_to_select).values 
            logger.info(f"Features selected: {top_10_features}") 
            top_10_df = balanced_df[top_10_features.tolist() + ['booking_status']]
            return top_10_df
        except Exception as e:
            logger.error(f"Error in feature selection: {e}")
            raise CustomException(e, sys)
            
    def save_data(self, df, filepath):
        try:
            logger.info(f"Saving processed data to {filepath}")
            df.to_csv(filepath, index=False)
            logger.info("Data saved successfully")
        except Exception as e:
            logger.error(f"Error in saving data: {e}")
            raise CustomException(e, sys) 
        
    def process(self):
        try:
            logger.info(f"Loading data from raw directory")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            
            train_df = self.preprocessed_data(train_df)
            test_df = self.preprocessed_data(test_df)
            
            train_df = self.balance_data(train_df)
            # test_df = self.balance_data(test_df)
            
            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]  # Ensure test_df has the same columns as train_df
            
            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)
            logger.info("Data processing completed successfully")
        except Exception as e:
            logger.error(f"Error in data processing: {e}")
            raise CustomException(e, sys) 
        
if __name__ == "__main__": 
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()
    logger.info("Data preprocessing script executed successfully")