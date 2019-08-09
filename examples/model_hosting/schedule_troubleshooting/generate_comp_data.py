import random
import string
from datetime import datetime, timedelta
from time import sleep

import pandas as pd
from cognite.client import CogniteClient
from cognite.client.stable.time_series import TimeSeries

client = CogniteClient()
NUMBER_OF_DATAPOINTS = 20000
prefix = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


def random_walk(min_val, max_val, num_of_points):
    points = [random.randrange(min_val, max_val)]
    for i in range(1, num_of_points):
        move = 1 if random.random() > 0.5 else -1
        point = points[i - 1] + move * random.random()
        points.append(max(min(point, max_val), min_val))
    return points


def fake_prod_rate(temp, pressure, rpm):
    return (temp + pressure) - (rpm * 0.5)


def generate_data():
    data = {}
    one_day_ago = datetime.now() - timedelta(days=1)
    one_day_ahead = datetime.now() + timedelta(days=1)
    one_day_ago_ms = int(round(one_day_ago.timestamp() * 1000))
    one_day_ahead_ms = int(round(one_day_ahead.timestamp() * 1000))
    step = (one_day_ahead_ms - one_day_ago_ms) // NUMBER_OF_DATAPOINTS

    data["timestamp"] = [timestamp for timestamp in range(one_day_ago_ms, one_day_ahead_ms, step)][
        :NUMBER_OF_DATAPOINTS
    ]
    data["{}_inlet_pressure".format(prefix)] = random_walk(75, 125, NUMBER_OF_DATAPOINTS)
    data["{}_outlet_pressure".format(prefix)] = random_walk(150, 300, NUMBER_OF_DATAPOINTS)

    df = pd.DataFrame(data)
    return df


def post_data(df):
    time_series_to_post = [TimeSeries(name=name) for name in df.columns if name != "timestamp"]
    # Create a time series for the cpr
    time_series_to_post.append(TimeSeries(name="{}_cpr".format(prefix)))

    client.time_series.post_time_series(time_series_to_post)

    created_time_series = []
    while len(created_time_series) != 3:
        created_time_series = client.time_series.get_time_series(prefix=prefix)
        sleep(0.5)

    client.datapoints.post_datapoints_frame(df)

    ts_dict = {"_".join(ts.name.split("_")[1:]): ts.id for ts in created_time_series}
    print(ts_dict)


if __name__ == "__main__":
    df = generate_data()
    post_data(df)
