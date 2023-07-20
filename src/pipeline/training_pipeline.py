import sys
import os
import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
try:
    if __name__=="__main__":
        obj=DataIngestion()
        train_data,test_data=obj.initiate_data_ingestion()
        data_tranformation=DataTransformation()
        train_arr,test_arr,obj_file_path=data_tranformation.initiate_data_trans(train_data,test_data)
        model_training =ModelTrainer()
        model_training.initiate_model_training(train_arr,test_arr)
except Exception as e:
    raise CustomException(e,sys)

