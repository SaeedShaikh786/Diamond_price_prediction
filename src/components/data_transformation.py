import os
import sys
import logging
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OrdinalEncoder
from sklearn.impute import SimpleImputer
from dataclasses import dataclass
from src.utils import save_obj


@dataclass
class DataTransformationconfig:
    preprocessor_obj_file_path=os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationconfig()   # obj for above class .

    def get_data_tranformation_obj(self):  # only to get the preprocessor object 
        try:
            logging.info("Data Transformation has started")
            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']
            
            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            # Numerical pipeline 
            num_pipline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median"))
                    ,("scalar",StandardScaler())
                ]
            )

            # Categorical Pipeline
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent"))
                    ,("Ordinalencoder",OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories]))
                    ,("scalar",StandardScaler())
                ]
            )

            ## now to combine those two pipeline
            preprocessor=ColumnTransformer([
            ("num_pipline",num_pipline,numerical_cols)
            ,("cat_pipeline",cat_pipeline,categorical_cols)
            ])
            
            logging.info("Pipeline completed")

            return preprocessor

        except Exception as e:
            logging.info("error in transformation")
            raise CustomException(e,sys)
    def initiate_data_trans(self,train_path,test_path):
        try:
            # reading the train and test data
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            
            logging.info("Read the train and test data")
            logging.info(f"Train dataset head : \n{train_df.head().to_string()}")
            logging.info(f"Test dataset head : \n{test_df.head().to_string()}")

            preprocessor_obj=self.get_data_tranformation_obj()

            target_column_name = 'price'
            drop_columns = [target_column_name,'id']

            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]

            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets.")

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
                    
            save_obj(
            file_path=self.data_transformation_config.preprocessor_obj_file_path
            ,obj=preprocessor_obj)

            logging.info("preprocessor pickle file saved")

            return (train_arr
            ,test_arr
            ,self.data_transformation_config.preprocessor_obj_file_path)

        except Exception as e:
            logging.info("Exception in initiate data trans function")
           
            raise CustomException(e,sys)

            



            
        
