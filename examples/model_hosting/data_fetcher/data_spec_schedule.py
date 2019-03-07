import os

from cognite.model_hosting.data_fetcher import DataFetcher
from cognite.model_hosting.data_spec import *

# Let's begin by defining our schedule data spec.
# This will describe what data we want to feed our model and how to traverse the data.
aggregate = "average"
granularity = "1m"

id_of_output_timeseries = 123

# We specify aliases for the time series so that we have human readable identifiers
schedule_data_spec = ScheduleDataSpec(
    input=ScheduleInputSpec(
        time_series={
            "gas_auto": ScheduleInputTimeSeriesSpec(5168669678602879, aggregate=aggregate, granularity=granularity),
            "gas_external": ScheduleInputTimeSeriesSpec(6811013084414704, aggregate=aggregate, granularity=granularity),
            "gas_delta_time": ScheduleInputTimeSeriesSpec(
                6894532287305357, aggregate=aggregate, granularity=granularity
            ),
            "gas_integ_time": ScheduleInputTimeSeriesSpec(
                4988486819178408, aggregate=aggregate, granularity=granularity
            ),
            "gas_gain": ScheduleInputTimeSeriesSpec(3658191334677419),
        }
    ),
    output=ScheduleOutputSpec({"transformed": ScheduleOutputTimeSeriesSpec(123)}),
    window_size="1h",  # This means we will feed our model with one minute of data every time it is run.
    stride="1h",  # This means our schedule will run once a minute.
    start="10d-ago",
)

# Now we can use this method to get the data specs that our model would be fed 10 days ago.
# This will yield 24 data specs.

data_specs = schedule_data_spec.get_instances(start="10d-ago", end="9d-ago")

# We can feed these data_specs to a DataFetcher and see exactly what data our model would receive 10 days ago for the
# "gas_auto" time series
first_data_spec = data_specs[0]
data_fetcher = DataFetcher(first_data_spec, api_key=os.getenv("COGNITE_OID_API_KEY"), project="publicdata")
print(data_fetcher.time_series.fetch_datapoints("gas_auto").head())
