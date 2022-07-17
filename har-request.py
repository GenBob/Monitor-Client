import requests
import pandas as pd
from datetime import timedelta


def call():
    df = pd.read_pickle("example_data.pk")
    df.loc[:, "ts"] = df.timestamp.apply(lambda x: timedelta(milliseconds=x / 100000)).cumsum()
    df = df.set_index("ts")
    df.columns = ["timestamp", "acc_x", "acc_y", "acc_z"]

    result = requests.post("https://secloud.informatik.uni-wuerzburg.de/monitor/har",
                           json={"acc": {"acc_x": df["acc_x"].values.tolist(),
                                         "acc_y": df["acc_y"].values.tolist(),
                                         "acc_z": df["acc_z"].values.tolist()},
                                 "timestamp": df["timestamp"].values.tolist(),
                                 "predict_frequency": 1,
                                 "secret": "<Enter-Secret>"},)
    activities = result.json()["activities"]
    return activities


if __name__ == '__main__':
    activities = call()
