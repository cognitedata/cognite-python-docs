import random
import string
from datetime import datetime, timedelta
from time import sleep

import numpy as np
import pandas as pd
from cognite.client import CogniteClient
from cognite.client.data_classes.time_series import TimeSeries


def random_sequence(n, minimum, maximum, variability, shift_ratio):
    values = []
    v = random.randrange(minimum, maximum)
    for i in range(n):
        values.append(v)

        if random.random() < shift_ratio:
            v += (random.random() - 0.5) * 0.5 * (maximum - minimum)
        else:
            v += (random.random() - 0.5) * variability * (maximum - minimum)

        if v > maximum:
            v -= (v - maximum) * 0.1
        if v < minimum:
            v += (minimum - v) * 0.1

    return np.array(values)


def generate_data():
    start = int((datetime(2019, 3, 1)).timestamp() * 1000)
    end = int((datetime(2019, 3, 3) + timedelta(hours=4)).timestamp() * 1000)

    data = {}
    timestamp = np.array(range(start, end, 5000))
    data["temperature"] = random_sequence(len(timestamp), 260, 350, 0.05, 0.001)
    data["pressure"] = random_sequence(len(timestamp), 150, 300, 0.01, 0.005)
    data["friction"] = (
        200
        - 1.58 * data["temperature"]
        + 1.34 * data["pressure"]
        + 0.96 * np.sqrt(data["temperature"] * data["pressure"])
        + 20 * np.sin(data["temperature"] + data["pressure"])  # Some unmodelled phenomena
    )

    data["temperature"] += np.random.randn(len(timestamp)) * 10
    data["pressure"] += np.random.randn(len(timestamp)) * 7
    data["friction"] += np.random.randn(len(timestamp)) * 15

    return pd.DataFrame(data, index=timestamp)


def post_data(df):
    prefix = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    ts_names = {
        "temperature": "tutorial_{}_temperature".format(prefix),
        "pressure": "tutorial_{}_pressure".format(prefix),
        "friction": "tutorial_{}_friction".format(prefix),
    }
    df.rename(columns=ts_names, inplace=True)

    client = CogniteClient()
    client.time_series.create([TimeSeries(name=name, external_id=name) for name in df.columns])

    created_time_series = []
    while len(created_time_series) != 3:
        created_time_series = client.time_series.search(name="tutorial_" + prefix)
        sleep(0.5)

    client.datapoints.insert_dataframe(df, external_id_headers=True)

    ts_ids = {ts.name.split("_", 2)[-1]: ts.id for ts in created_time_series}
    return ts_ids


if __name__ == "__main__":
    df = generate_data()
    ts_ids = post_data(df)
    print(ts_ids)
