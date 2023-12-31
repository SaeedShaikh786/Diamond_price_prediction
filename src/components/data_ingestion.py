import os
import sys
import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation

# initiate data ingestion configuration

@dataclass
class DataIngestionconfig:
    train_data_path:str=os.path.join("artifacts","train.csv")
    test_data_path:str=os.path.join("artifacts","test.csv")
    raw_data_path:str=os.path.join("artifacts","raw.csv")

## create a class for data ingestion

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionconfig()    # this will have all three above paths in tuple form 
    
    def initiate_data_ingestion(self):
        logging.info("data ingestion has started")
        try:
            df=pd.read_csv(os.path.join("notebooks/data","gemstone.csv"))
            logging.info("Dataset read as Pd dataframe")
            # now we will make directory for raw data path
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False)

            logging.info("Train test split")

            train_set,test_set=train_test_split(df,test_size=0.30,random_state=32)  # it will give 2 or 4 output varible

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of data is completed")
            
            #Now we return the train and test data paths
            return (self.ingestion_config.train_data_path,self.ingestion_config.test_data_path)

        except Exception as e:
            logging.info("Exception in data ingestion")
            raise CustomException(e,sys)
        




            