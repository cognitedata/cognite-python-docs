import os

from cognite.model_hosting.data_fetcher import DataFetcher
from cognite.model_hosting.data_spec import *

# Let's begin by defining our data spec
start = "10d-ago"
end = "now"
aggregate = "average"
granularity = "1m"

# We specify aliases for the time series so that we have human readable identifiers
data_spec = DataSpec(
    time_series={
        "gas_auto": TimeSeriesSpec(
            id=5168669678602879, start=start, end=end, aggregate=aggregate, granularity=granularity
        ),
        "gas_external": TimeSeriesSpec(
            id=6811013084414704, start=start, end=end, aggregate=aggregate, granularity=granularity
        ),
        "gas_delta_time": TimeSeriesSpec(
            id=6894532287305357, start=start, end=end, aggregate=aggregate, granularity=granularity
        ),
        "gas_integ_time": TimeSeriesSpec(
            id=4988486819178408, start=start, end=end, aggregate=aggregate, granularity=granularity
        ),
        "gas_gain": TimeSeriesSpec(id=3658191334677419, start=start, end=end),
    }
)


# Now lets fetch the data for our "gas_auto" and "gas_external" time series
data_fetcher = DataFetcher(
    data_spec, api_key=os.getenv("COGNITE_OID_API_KEY"), project="publicdata", client_name="test-client"
)


df = data_fetcher.time_series.fetch_dataframe(["gas_auto", "gas_external"])

print(df.head())


# When using fetch_dataframe all specified time series must have the same start, end, and granularity
# To fetch data from times series with different specs, we can use the following method

dfs = data_fetcher.time_series.fetch_datapoints(["gas_integ_time", "gas_gain"])

print(dfs["gas_gain"].head())
print(dfs["gas_integ_time"].head())
