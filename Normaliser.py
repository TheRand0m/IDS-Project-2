
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
import numpy as np

class Normaliser:
    def __init__(self):
        self.minMaxScaler = MinMaxScaler()

    def scale(self, dataframe):
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
        X_features = dataframe.drop(['label'], axis='columns')
        X_normalised = self.minMaxScaler.fit_transform(X_features)
        return X_normalised

