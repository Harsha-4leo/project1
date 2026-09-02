import os
import sys
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_models,save_object

from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor,RandomForestRegressor,GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score

@dataclass
class ModeltrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')

class Modeltrainer:
    def __init__(self):
        self.model_trainer_config = ModeltrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Training has started")
            X_train,y_train,X_test,y_test = (train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1])

            models = {
                "LinearRegressor": LinearRegression(),
                "Ridge": Ridge(),
                "Lasso": Lasso(),
                "CatBoostRegressor": CatBoostRegressor(),
                "ElasticNet": ElasticNet(),
                "DecisionTreeRegressor": DecisionTreeRegressor(),
                "AdaBoostRegressor": AdaBoostRegressor(),
                "RandomForestRegressor": RandomForestRegressor(),
                "GradientBoostingRegressor": GradientBoostingRegressor(),
                "KNeighborsRegressor": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
            }
            model_report =evaluate_models(X_train,y_train,X_test,y_test,models)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
                ]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No Best Model Found")

            logging.info("Best Model Found on the data set")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj= best_model
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test,predicted)
            return r2_square
        
        except Exception as e:
            raise CustomException(e,sys)
        