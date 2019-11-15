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
    start = int((datetime.now() - timedelta(hours=4)).timestamp() * 1000)
    end = int((datetime.now() + timedelta(hours=4)).timestamp() * 1000)

    data = {}
    timestamp = np.array(range(start, end, 1000))
    data["x"] = random_sequence(len(timestamp), 260, 350, 0.05, 0.001)
    data["y"] = random_sequence(len(timestamp), 150, 300, 0.01, 0.005)

    return pd.DataFrame(data, index=timestamp)


def post_data(df):
    prefix = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    ts_names = {"x": "tutorial_{}_x".format(prefix), "y": "tutorial_{}_y".format(prefix)}
    df.rename(columns=ts_names, inplace=True)

    client = CogniteClient()
    client.time_series.create([TimeSeries(name=name, external_id=name) for name in df.columns])
    output_ts_name = "tutorial_{}_mean_x_y".format(prefix)
    client.time_series.create([TimeSeries(name=output_ts_name, external_id=output_ts_name)])

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
