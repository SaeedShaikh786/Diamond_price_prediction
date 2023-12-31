from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet
from src.exception import CustomException
from src.logger import logging

from src.utils import save_obj
from src.utils import evaluate_model
from dataclasses import dataclass
import sys
import os

@dataclass
class ModelTrainerconfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerconfig()

    def initiate_model_training(self,train_arr,test_arr):
        try:
            logging.info("splititng the data into train test ")
            X_train,y_train,X_test,y_test=train_arr[:,:-1],train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1]

            models={
                "Linear Regression":LinearRegression(),"Lasso":Lasso()
                ,"Ridge":Ridge()
                ,"Elasticnet":ElasticNet()
            }
            model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models)
            print(model_report)
            print("/n============================================")
            logging.info(f"model report :{model_report}")

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]

            print(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')

            save_obj(file_path=self.model_trainer_config.trained_model_file_path,obj=best_model)


        except Exception as e:
            logging.info("error in model trainer")
            raise CustomException(e,sys)
