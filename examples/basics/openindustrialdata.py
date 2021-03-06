import os

import matplotlib.pyplot as plt
from cognite.client import CogniteClient

client = CogniteClient(api_key=os.getenv("COGNITE_API_KEY"), project="publicdata")

# Retrieve one year of daily aggregates for a time series
ts = "VAL_23-PT-92512:X.Value"
dataframe = client.datapoints.get_datapoints_frame(
    [ts], start="52w-ago", aggregates=["avg", "min", "max"], granularity="1d", processes=1
)

# Plot the dataframe
dataframe.plot(x="timestamp")
plt.show()
