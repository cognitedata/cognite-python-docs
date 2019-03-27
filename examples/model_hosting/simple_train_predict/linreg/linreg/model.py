import numpy as np
import pandas as pd
from cognite.model_hosting.data_fetcher import DataFetcher


class Model:
    """
    You need to have a class called Model in a file called model.py at the 
    top level of your package.

    It should contain
        - Static train method
            Which performs training and persist any state you need for
            prediction. This can be serialized models, csv, or something else.
            You just have to be able to store it in files.
        - Static load method
            Which loads your persisted state and return an instance of the Model
            class that are ready for predictions.
        - Predict method
            Which use the persisted state to do predictions.

    """

    @staticmethod
    def train(open_artifact, data_spec):
        """
        open_artifact:
            The train method must accept a open_artifact argument. This is a function
            that works the same way as the builtin open(), except it reads from
            and writes to the root of a special storage location in the cloud
            that belongs to the current model version.
        data_spec:
            An argument we pass in ourself when we initiate the training.
        api_key, project:
            Optional arguments that are passed in automatically from Model
            Hosting if you specify them.
        """
        data_fetcher = DataFetcher(data_spec)
        data_fetcher.files.fetch("data")
        data_fetcher.files.fetch("target")

        X = pd.read_csv("data")
        y = pd.read_csv("target")

        # Add a feature of constant value 1
        X.insert(0, "f0", 1)

        # Least squares
        coefficients = pd.DataFrame(np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y), columns=["beta_hat"])

        # Persist our result
        with open_artifact("coefficients.csv", "w") as f:
            coefficients.to_csv(f, index=False)

    def __init__(self, coefficients):
        self.coefficients = coefficients

    @staticmethod
    def load(open_artifact):
        """
        We'll use open_artifact to access and load the coefficients we found during
        training. We then return an instance of the Model class that is used
        for doing predictions.
        """
        with open_artifact("coefficients.csv", "r") as f:
            coefficients = pd.read_csv(f)
        return Model(coefficients)

    def predict(self, instance, precision=2):
        """
        instance:
            The value we want to do prediction on. In our case this is a list
            of two numbers.
        precision:
            Optional argument we have defined ourselves.
        
        Note that it's also possible to take api_key and project in as
        optional arguments here the same way as in train().
        """
        instance = pd.DataFrame([[1] + instance], columns=["f0", "f1", "f2"])
        prediction = float(np.dot(instance, self.coefficients))
        prediction = round(prediction, precision)
        return prediction
