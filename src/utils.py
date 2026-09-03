import os
import sys
import dill
from src.exception import CustomException

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys)

def evaluate_models(X_train,y_train,X_test,y_test,model):
    try:
        for name , type in model.items():
            type.fit(X_train,y_train)

            y_train_pred = type.predict(X_train)
            y_test_pred = type.predict(X_test)

            train_score = r2_score(y_train,y_train_pred)
            test_score = r2_score(y_test,y_test_pred)

            return {name: test_score}

    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e,sys)



        