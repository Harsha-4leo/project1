import sys
from dataclasses import dataclass
import os


import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str= os.path.join('artifacts','processor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformation(self):
        try:

            num_columns = ['carat','depth','table','x','y','z']
            cat_columns = ['cut','color','clarity']

            num_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('onehotencoder',OneHotEncoder())
                ]
            )
            logging.info("Numerical columns  scaling completed")
            logging.info("Categorical columns scalling completed")
            processor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_columns),
                    ("cat_pipeline",cat_pipeline,cat_columns)
            
                ]
            )
            logging.info("Transformation completed")

            return processor

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and Test Data")

            logging.info("Obtaining processor")

            processor_obj=self.get_data_transformation()

            input_train = train_df.drop(['price'],axis=1)
            target_train = train_df['price']

            input_test = test_df.drop(['price'],axis=1)
            target_test = test_df['price']

            transformed_train = processor_obj.fit_transform(input_train)
            transformed_test  = processor_obj.transform(input_test)

            train_arr = np.c_[transformed_train,np.array(target_train)]
            test_arr = np.c_[transformed_test,np.array(target_test)]

            logging.info("Processing saved")

            save_object(

                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj=processor_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)


