class Sanitiser:
    def __init__(self):
        print("Initialised Sanitiser")

    def sanitise(self,dataframe):
        # Replaces the hyphen which represents as null in the dataset with python version of null.
        return dataframe.replace('-', None)

    def removeNullColumns(self, dataframe):
        columns_to_remove = self.countNulls(dataframe)
        print("Removing columns:", columns_to_remove)
        new_dataframe = dataframe.drop(columns=columns_to_remove)
        return new_dataframe


    def removeNullValue(self, dataframe, columns):
        print("Clearing null rows in:", columns)
        dataframe.dropna(subset=columns)

        return dataframe
