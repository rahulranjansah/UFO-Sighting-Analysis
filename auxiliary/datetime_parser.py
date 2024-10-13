# standard imports
from datetime import timedelta
import doctest
import pandas as pd

def custom_to_datetime(date: str) -> pd.Timestamp:
    """
    Converts a date string to a pandas datetime dtype.

    Parameters
    ----------
    date : str
        A date string to be parsed and converted to datetime.

    Returns
    -------
    pd.Timestamp
        A pandas Timestamp object representing the datetime.

    Notes
    -----
    This function handles cases where the hour part of the time is '24' and increments the day by
    one, setting the time to '00:00:00'.

    Examples
    --------
    >>> custom_to_datetime("1/1/1952 24:00")
    Timestamp('1952-01-02 00:00:00')

    >>> custom_to_datetime("1/1/1952 2:00:00")
    Timestamp('1952-01-01 02:00:00')

    >>> custom_to_datetime("1/1/1952 12:00")
    Timestamp('1952-01-01 12:00:00')

    >>> custom_to_datetime("invalid date")
    Traceback (most recent call last):
        ...
    pandas._libs.tslibs.parsing.DateParseError: Unknown datetime string format,
    unable to parse: invalid date, at position 0
    """
    # Handle different date formats
    try:
        if date[11:13] == "24":
            base_date = pd.to_datetime(date[:11])
            new_date = base_date + timedelta(days=1)
            x = new_date.strftime('%m/%d/%Y') + " 00:00:00"
        elif date[10:12] == "24":
            base_date = pd.to_datetime(date[:10])
            new_date = base_date + timedelta(days=1)
            x = new_date.strftime('%m/%d/%Y') + " 00:00:00"
        elif date[9:11] == "24":
            base_date = pd.to_datetime(date[:9])
            new_date = base_date + timedelta(days=1)
            x = new_date.strftime('%m/%d/%Y') + " 00:00:00"
        else:
            return pd.to_datetime(date)
    except ValueError:
        if "24:00" in date:
            new_date = base_date + timedelta(days=1)
            x = new_date.strftime('%m-%d-%Y') + " 00:00:00"
        else:
            return pd.to_datetime(date)

    return pd.to_datetime(x)


if __name__ == "__main__":
    doctest.testmod()
