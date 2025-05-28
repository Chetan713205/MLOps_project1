import os
import sys
import mlflow.artifacts
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint
import mlflow
import mlflow.sklearn 

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        
        self.param_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS 
        
    def load_and_split_data(self):
        try:
            logger.info(f"Loading training data from {self.train_path}")
            train_df = load_data(self.train_path)
            logger.info(f"Loading test data from {self.test_path}")
            test_df = load_data(self.test_path)
            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']
            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']
            logger.info(f"Data loaded successfully with shapes: X_train: {X_train.shape}, y_train: {y_train.shape}, X_test: {X_test.shape}, y_test: {y_test.shape}")
            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise CustomException(f"Error loading data: {e}", sys)
        
    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Starting LightGBM model training")
            lgbm_model = lgb.LGBMClassifier(random_state = self.random_search_params['random_state']) 
            logger.info("Setting up RandomizedSearchCV for hyperparameter tuning") 
            random_search = RandomizedSearchCV(
                estimator = lgbm_model,
                param_distributions = self.param_dist,
                n_iter = self.random_search_params['n_iter'],
                scoring = self.random_search_params['scoring'],
                cv = self.random_search_params['cv'],
                n_jobs= self.random_search_params['n_jobs'],
                verbose = self.random_search_params['verbose'],
                random_state = self.random_search_params['random_state']
            )
            logger.info("Starting our Hyperparameter tuning")
            random_search.fit(X_train, y_train)
            logger.info("Model training completed successfully")
            best_params = random_search.best_params_
            best_lbgm_model = random_search.best_estimator_
            logger.info(f"Best parameters found: {best_params}")
            return best_lbgm_model
        except Exception as e:  
            logger.error(f"Error during model training: {e}")
            raise CustomException(f"Error during model training: {e}", sys)
        
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating the trained model")
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            logger.info(f"Model evaluation metrics - Accuracy: {accuracy}, F1 Score: {f1}, Precision: {precision}, Recall: {recall}")
            return {
                "accuracy" : accuracy, 
                "f1 score" : f1, 
                "precision" : precision, 
                "recall" : recall
            }
        except Exception as e:
            logger.error(f"Error during model evaluation: {e}")
            raise CustomException(f"Error during model evaluation: {e}", sys)
        
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True) 
            joblib.dump(model, self.model_output_path) 
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise CustomException(f"Error saving model: {e}", sys)
        
    def run(self):
        try:
            with mlflow.start_run(): 
                logger.info(f"Starting ML-FLOW experimentation")
                logger.info("Logging the train and test daata to ML-FLOW")
                mlflow.log_artifact(self.train_path, artifact_path="datasets") 
                mlflow.log_artifact(self.test_path, artifact_path="datasets")
                
                X_train, y_train, X_test, y_test = self.load_and_split_data()
                best_lbgm_model = self.train_lgbm(X_train, y_train)
                metrics = self.evaluate_model(best_lbgm_model, X_test, y_test)
                self.save_model(best_lbgm_model)
                
                logger.info("Logging the model to ML-FLOW") 
                mlflow.log_artifact(self.model_output_path)
                logger.info("Logging model parameters and metrics to ML-FLOW") 
                mlflow.log_params(best_lbgm_model.get_params())
                mlflow.log_metrics(metrics) 
                logger.info(f"Model training and evaluation completed successfully with metrics: {metrics}")
        except CustomException as ce:
            logger.error(f"Custom exception occurred: {ce}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise CustomException(f"An unexpected error occurred: {e}", sys)
        
if __name__ == "__main__":
    trainer = ModelTraining(
        train_path=PROCESSED_TRAIN_DATA_PATH,
        test_path=PROCESSED_TEST_DATA_PATH,
        model_output_path=MODEL_OUTPUT_PATH
    )
    trainer.run()
    
    
