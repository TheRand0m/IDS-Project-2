class Analyzer:
    def __init__(self):
        print(" ")

    def probeUniqueValues(self, dataframe):
        for column in dataframe.columns:
            unique_count = dataframe[column].nunique()
            if unique_count < 60:
                print(column, unique_count, dataframe[column].unique())
                # print(cell_df[column].value_counts())
            else:
                print(column, unique_count)

    def countNulls(self, dataframe):
        print("--------[ Checking for nulls in columns ]--------")
        null_columns=[]
        for column in dataframe.columns:
            null_values = dataframe[column].isnull().sum()
            total_values = len(dataframe[column])  # Count total number of rows
            difference = (null_values / total_values) * 100

            print("Column:", column, "Nulls:", null_values, "Total:", total_values, "(", difference, "%)")

            if difference > 60:
                null_columns.append(column)

        print(null_columns)
        return null_columns


    def removeNullColumns(self, dataframe):
        print("--------[ Removing nulls in columns ]--------")
        columns_to_remove = self.countNulls(dataframe)
        print("Removing columns:", columns_to_remove)
        new_dataframe = dataframe.drop(columns=columns_to_remove)
        return new_dataframe


    def removeNullValue(self, dataframe, columns):
        print("--------[ Removing nulls in rows ]--------")
        print("Clearing null rows in:", columns)
        dataframe.dropna(subset=columns)

        return dataframe

    def calculateDistribution(self, dataframe):
        total = total_rows = len(dataframe)
        malicious = (dataframe['label'] == 1).sum()
        normal = (dataframe['label'] == 0).sum()

        malicious_percentage = (malicious / total_rows) * 100
        normal_percentage = (normal / total_rows) * 100

        print("Malicious: ", malicious, "(", malicious_percentage, "%)")
        print("Normal: ", normal, "(", normal_percentage, "%)")
