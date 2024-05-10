import csv
from joblib import dump, load
import sys
import pandas as pd
import os
import time

from Preprocessing import Preprocessor
from Analyzer import Analyzer
from TrainAndTester import TrainTester

class IntrusionDetector:
    def __init__(self):
        self.model_path = "TrainedModel.model"
        self.path = ""
        self.dataframe = pd.DataFrame()
        self.script_root = os.path.realpath(__file__)
        self.analyzer = Analyzer()
        self.debug = True

    def preprocess(self):
        print("Processing dataset...")
        self.dataframe = Preprocessor(self.dataframe).process()


    def persistence_load(self):
            if os.path.isfile(self.model_path):
                print("Found existing model.")
                self.model = load(self.model_path)
                print("Previous model found and loaded successfully.")
                return self.model

    def persistence_save(self):
        dump(self.model, self.model_path)

    def saveResultsToCSV(self, dataframe):
        print("Saving results")
        filename = os.path.basename(self.path)
        outputPath = os.path.join("processed", 'RESULTS-' + filename)
        dataframe.to_csv(outputPath, index=False)

    def gridSearch(self):
        initial_time = time.time()

        self.dataframe = pd.read_csv(self.path, delimiter="|")

        self.dataframe = Preprocessor(self.dataframe).process()

        TrainTester(self.dataframe).gridsearch()

        print("Finished in:", time.time() - initial_time)

    def SVM_Train(self):
        initial_time = time.time()
        print("Reading CSV: ", self.path)
        self.dataframe = pd.read_csv(self.path, delimiter="|")

        self.dataframe = Preprocessor(self.dataframe).process()

        print(self.dataframe.head())
        model = TrainTester(self.dataframe).train()
        dump(model, self.model_path)
        print("Model saved.")
        print("Finished in:", time.time() - initial_time)

    def SVM_Test(self):

        initial_time = time.time()
        self.persistence_load()
        self.dataframe = pd.read_csv(self.path, delimiter="|")

        self.dataframe = Preprocessor(self.dataframe).process()

        if self.debug:
            results = self.analyzer.calculateDistribution(self.dataframe)
            time.sleep(2)

        malicious_data = TrainTester(self.dataframe).test(self.model_path)

        self.saveResultsToCSV(malicious_data)

        print("Saved at:", os.path.basename(self.path))
        print("Finished in:", time.time() - initial_time)
        return True

    def print_menu(self):
        print("1. Train model. \n2. Test dataset. \n3. Fetch optimised SVC parameters.\n 4. Quit\n")


def main():
    mIntrusionDetector = IntrusionDetector()

    if len(sys.argv) > 1:
        # Check if the script started with the parameters ./Main.py --api
        if not sys.argv[1] == "--api":
            return

        csv_file_path = sys.argv[2]

        mIntrusionDetector.path = os.path.join(os.path.dirname(mIntrusionDetector.script_root), "toProcess", sys.argv[2])
        print(sys.argv[2])
        results = mIntrusionDetector.SVM_Test()
        print("Done!")

    else:
        mIntrusionDetector.print_menu()
        selection = 1
        while selection < 4:
            selection = int(input("Enter option: "))
            if selection == 1:
                mIntrusionDetector.path = input("Enter CSV path: ")
                mIntrusionDetector.SVM_Train()
                break
            if selection == 2:
                mIntrusionDetector.path = input("Enter dataset to test: ")
                mIntrusionDetector.SVM_Test()
                break
            if selection == 3:
                mIntrusionDetector.path = input("Enter dataset to test: ")
                mIntrusionDetector.gridSearch()
                break

    print("Good bye!")

if __name__ == "__main__":
    main()
