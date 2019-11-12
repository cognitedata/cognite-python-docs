import os
from datetime import datetime

from cognite.model_hosting.data_fetcher import DataFetcher
from cognite.model_hosting.data_spec import *

# Let's begin by defining our schedule data spec.
# This will describe what data we want to feed our model and how to traverse the data.
aggregate = "average"
granularity = "15m"

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
    output=ScheduleOutputSpec({"transformed": ScheduleOutputTimeSeriesSpec(id_of_output_timeseries)}),
    window_size="1h",  # We will feed our model with 4 data points (since window_size is 1h and granularity is 15m)
    stride="1h",  # This means our schedule will run once an hour
    start=datetime(2019, 1, 1),
)

# Now we get the data specs that our model would be fed on the 10th of January
# This will return 24 data specs, since the stride is set to 1 hour. Stride set to 8 hours would return 3 data specs.

data_specs = schedule_data_spec.get_instances(start=datetime(2019, 1, 10), end=datetime(2019, 1, 11))

# We feed these data_specs to a DataFetcher and see exactly what data our model would receive on the 10th of January
first_data_spec = data_specs[0]
data_fetcher = DataFetcher(
    first_data_spec, api_key=os.getenv("COGNITE_OID_API_KEY"), project="publicdata", client_name="test-client"
)
print(data_fetcher.time_series.fetch_datapoints("gas_auto").head())
