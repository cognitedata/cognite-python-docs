import pickle

from cognite.model_hosting.data_fetcher import DataFetcher
from cognite.model_hosting.schedules import to_output


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
            Which load your persisted state and return an instance of the Model
            class that are ready for predictions.
        - Predict method
            Which use the persisted state to do predictions.

    """

    def __init__(self, regressor):
        self.regressor = regressor

    @staticmethod
    def load(open_artifact):
        """
        We'll use open_artifact to access and load the regressor we fitted during
        training. We then return an instance of the Model class that are ready
        for doing predictions.
        """
        with open_artifact("regressor.pickle", "rb") as f:
            regressor = pickle.load(f)
        return Model(regressor)

    def predict(self, instance):
        """
        instance:
            Since we're doing scheduled prediction, this will be a data spec
            describing the data we should do prediction on.
        
        Note that it's also possible to take api_key and project in as
        optional arguments here.
        """
        dts = DataFetcher(instance)
        df = dts.time_series.fetch_dataframe(["temp", "pressure", "rpm"]).dropna()

        X = df[["temp", "pressure", "rpm"]].values
        df["production_rate"] = self.regressor.predict(X)

        # For scheduled prediction we need to return output on the format:
        # {
        #   "timeSeries":
        #      { "production_rate": [(t0, p0), (t1, p1), (t2, p2), ...] }
        # }
        # We can use a model hosting utilities method to convert our dataframe
        # to this format.
        return to_output(df[["timestamp", "production_rate"]])
