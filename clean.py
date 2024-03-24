import pandas as pd
import numpy as np

def raw_data_cleaner(df):

    """
    Function for building datetime series, numeric series, string series for respective features
    """

    def custom_to_datetime(date):
        """
        Datetime series hour, min, sec tool
        """
        if date[11:13] == "24":
            x = date[:11] + "23:59"
        elif date[10:12] == "24":
            x = date[:10] + "23:59"
        elif date[9:11] == "24":
            x = date[:9] +  "23:59"
        else:
            return pd.to_datetime(date)

        return pd.to_datetime(x)

    # setting numeric_val and cleaning position dtypes
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["lognitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["duration (seconds)"] = pd.to_numeric(df["duration (seconds)"], errors="coerce")

    df.loc[:,"latitude"].replace({0.0: np.nan}, inplace=True)
    df.loc[:, "longitude"].replace({0.0: np.nan}, inplace=True)
    df.loc[:,"duration (seconds)"].replace({0.0: np.nan}, inplace=True)
    df.index = np.arange(0, len(df))

    # string series dtype for comments
    df["comments"] = df["comments"].astype(str)

    # initialzing datetime series with time of report
    df["datetime"] = df["datetime"].apply(custom_to_datetime)
    df["date posted"] = pd.to_datetime(df["date posted"])

    df["month"] = pd.DatetimeIndex(df["datetime"]).month
    df["year"] = pd.DatetimeIndex(df["datetime"]).year
    df["day"] = pd.DatetimeIndex(df["datetime"]).day
    df["hour"] = pd.DatetimeIndex(df["datetime"]).hour

    return df

