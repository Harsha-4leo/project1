import sys
import os
import pandas as pd
from src.utils import load_object
from src.exception import CustomException

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path = 'artifacts\model.pkl'
            preprocessor_path = 'artifacts\processor.pkl'

            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            data_scaled = preprocessor.transform(features)

            pred = model.predict(data_scaled)
            return pred

        except Exception as e:
            raise CustomException(e,sys)

class CustomData:
    def __init__(self,
        carat:float,
        cut:str,
        color:str,
        clarity:str,
        depth:float,
        table:float,
        x:float,
        y:float,
        z:float):

        self.carat = carat
        self.cut = cut
        self.color = color
        self.clarity = clarity
        self.depth = depth
        self.table = table
        self.x = x
        self.y = y
        self.z = z

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "carat":[self.carat],
                "cut":[self.cut],
                "color":[self.color],
                "clarity":[self.clarity],
                "depth":[self.depth],
                "table":[self.table],
                "x":[self.x],
                "y":[self.y],
                "z":[self.z]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e,sys)

