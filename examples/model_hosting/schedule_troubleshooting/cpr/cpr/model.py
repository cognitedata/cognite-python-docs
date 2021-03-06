from cognite.model_hosting.data_fetcher import DataFetcher
from cognite.model_hosting.schedules import to_output


class Model:
    @staticmethod
    def load(open_artifact):
        return Model()

    def predict(self, instance):
        data_fetcher = DataFetcher(instance, client_name="cpr-client")
        df = data_fetcher.time_series.fetch_dataframe(["x1", "x2"])
        df["y"] = df["x2"] / df["x1"]

        return to_output(df.size)
