import os
import sys

import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))): # Iterate over models
            model = list(models.values())[i] # Get model
            para = param[list(models.keys())[i]] # Get model parameters

            gs = GridSearchCV(model, para, cv=3) # Grid search
            gs.fit(X_train, y_train) # Fit model

            model.set_params(**gs.best_params_) # Set best parameters
            model.fit(X_train, y_train) # Train model

            y_train_pred = model.predict(X_train) # Predict on train data
            y_test_pred = model.predict(X_test) # Predict on test data
            train_model_score = r2_score(y_train,y_train_pred) # Calculate R2 score on train data
            test_model_score = r2_score(y_test,y_test_pred) # Calculate R2 score on test data
            report[list(models.keys())[i]] = test_model_score # Save R2 score in report dictionary
        
        return report
    
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    
    except Exception as e:
        raise CustomException(e, sys)