from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from Sanitiser import Sanitiser
from Analyzer import Analyzer
import pandas as pd

class Preprocessor:
    def __init__(self, dataframe):
        self.label_encoder = LabelEncoder()
        self.minMaxScaler = MinMaxScaler()
        self.analyser = Analyzer()
        self.sanitiser = Sanitiser()
        self.dataframe = dataframe


    def sanitise(self):
        self.dataframe = self.dataframe.replace('-', None)

    def encode_feature(self, column):
        return self.label_encoder.fit_transform(column)

    def process(self):
        # Step 1 - Sanitise the dataset. Replace null values.
        self.sanitise()

        # Step 2 - Clear majority null columns
        self.analyser.countNulls(self.dataframe)
        self.dataframe = self.analyser.removeNullColumns(self.dataframe)

        # Step 3 - Clear null values
        self.dataframe = self.dataframe.dropna(subset=['history'])
        print(self.dataframe.isnull().sum())


        # Step 4 - For each X-feature in the dataframe/data set, check if
        # the value is numerical, if not then encode the entire column.
        for column in self.dataframe.columns:
            if not pd.api.types.is_numeric_dtype(self.dataframe[column]):
                self.dataframe[column] = self.encode_feature(self.dataframe[column])


        return self.dataframe
