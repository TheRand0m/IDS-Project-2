
from Normaliser import Normaliser
from Analyzer import Analyzer
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split, cross_val_score, KFold, GridSearchCV
from sklearn.svm import SVC
from joblib import dump, load
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import os



#
class TrainTester:
    def __init__(self, dataframe):
        self.SVM = SVC()
        self.normaliser = Normalizer()
        self.analyzer = Analyzer()
        self.dataframe = dataframe
        self.debug = False
        self.output_path = "processed/"

    def train(self):
        X = self.dataframe.drop('label', axis='columns')
        Y = self.dataframe['label']

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        X_train_normalised = self.normaliser.fit_transform(X_train)
        X_test_normalised = self.normaliser.fit_transform(X_test)

        SVM = SVC(kernel='linear', C=0.01, gamma='auto')
        SVM.fit(X_train_normalised, Y_train)

        Y_prediction = SVM.predict(X_test)

        accuracy = accuracy_score(Y_test, Y_prediction)
        report = classification_report(Y_test, Y_prediction)
        confusion_matrix = confusion_matrix(Y_test, Y_prediction)

        if self.debug:
            print(f"Accuracy: {accuracy}")
            print(f"Classification Report:\n{report}")

        return SVM


    def gridsearch(self):
        parameters = {'C': [0.1, 1, 10, 100, 1000]}

        X = self.dataframe.drop('label', axis='columns')
        Y = self.dataframe['label']

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        parameters = { 'C': [0.1, 1, 10, 100, 1000] }

        X_train_normalised = self.normaliser.fit_transform(X_train)
        X_test_normalised = self.normaliser.fit_transform(X_test)

        gridSearch = GridSearchCV(SVC(), parameters, n_jobs=-1, refit=True, verbose=3, cv=2)
        gridSearch.fit(X_train_normalised, Y_train)

        accuracy_scores = gridSearch.cv_results_['mean_test_score']

        print(gridSearch.best_params_)


    def gridsearch_C(self):
        parameters = {'C': [0.1, 1, 10, 100, 1000]}

        X = self.dataframe.drop('label', axis='columns')
        Y = self.dataframe['label']

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        X_train_normalised = self.normaliser.fit_transform(X_train)
        X_test_normalised = self.normaliser.fit_transform(X_test)

        gridSearch = GridSearchCV(SVC(), parameters, n_jobs=-1, refit=True, verbose=3, cv=2)
        gridSearch.fit(X_train_normalised, Y_train)

        accuracy_scores = gridSearch.cv_results_['mean_test_score']

        print(gridSearch.best_params_)
        self.plot(accuracy_scores,[0.1, 1, 10, 100, 1000], "CV Accuracy Score", "C-Parameter")

    def gridsearch_kernel(self):
        parameters = {'kernel':('linear', 'rbf', 'poly')}

        X = self.dataframe.drop('label', axis='columns')
        Y = self.dataframe['label']

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)



        X_train_normalised = self.normaliser.fit_transform(X_train)
        X_test_normalised = self.normaliser.fit_transform(X_test)

        gridSearch = GridSearchCV(SVC(), parameters, n_jobs=-1, refit=True, verbose=3, cv=2)
        gridSearch.fit(X_train_normalised, Y_train)

        accuracy_scores = gridSearch.cv_results_['mean_test_score']

        print(gridSearch.best_params_)
        self.plot(accuracy_scores, ['linear', 'rbf', 'poly'], "CV Accuracy Score", "Kernel")


    def gridsearch_gamma(self):
        parameters = {'gamma': [0.0001, 0.001, 0.01, 0.1, 1]}

        X = self.dataframe.drop('label', axis='columns')
        Y = self.dataframe['label']

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)



        X_train_normalised = self.normaliser.fit_transform(X_train)
        X_test_normalised = self.normaliser.fit_transform(X_test)

        gridSearch = GridSearchCV(SVC(), parameters, n_jobs=-1, refit=True, verbose=3, cv=2)
        gridSearch.fit(X_train_normalised, Y_train)

        accuracy_scores = gridSearch.cv_results_['mean_test_score']

        print(gridSearch.best_params_)
        self.plot(accuracy_scores, [0.0001, 0.001, 0.01, 0.1, 1], "CV Accuracy Score", "Gamma")


    def test(self, model):

        SVM = load(model)

        # Prepare dataset
        X_test = self.dataframe.drop('label', axis='columns')
        Y_test = self.dataframe['label']
        X_test_normalised = self.normaliser.transform(X_test)

        # Make predictions
        Y_prediction = SVM.predict(X_test_normalised)

        malicious_data = self.dataframe[self.dataframe['label'] == 1]

        # Print five rows where the predicted label is 1
        # Calculate accuracy and generate classification report
        accuracy = accuracy_score(Y_test, Y_prediction)
        report = classification_report(Y_test, Y_prediction)
        confusion_matrix = confusion_matrix(Y_test, Y_prediction)

        if self.debug:
            self.analyzer.calculateDistribution(self.dataframe)

            print(f"Accuracy: {accuracy}")
            print(f"Classification Report:\n{report}")

        return malicious_data

    def plot(self, X, Y, title, X_label, Y_label):
        plt.plot(X, Y)
        plt.xlabel(X_label)
        plt.ylabel(Y_label)
        plt.show()





