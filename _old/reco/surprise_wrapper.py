import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, RegressorMixin

from surprise import Dataset
from surprise import Reader

class SurpriseRecommender(BaseEstimator, RegressorMixin):
    def __init__(self, rating_scale, model):
        self.rating_scale = rating_scale
        self.reader = Reader(rating_scale = rating_scale)
        self.model = model

    def fit(self, X, y):
        df = pd.DataFrame(X)
        df["rating"] = y
        trainset = Dataset.load_from_df(df, self.reader).build_full_trainset()
        self.model.fit(trainset)
        return(self)

    def predict(self, X):
        df = pd.DataFrame(X)
        df["rating"] = 0
        prediction_df = pd.DataFrame(
            self.model.test(
                Dataset.load_from_df(df, self.reader)
                .build_full_trainset()
                .build_testset()
            )
        )
        prediction_array = prediction_df["est"].values
        return(prediction_array)
