from math import isnan
from icecream import ic
import pandas as pd
import numpy as np
from utils import R_to_col, TOKEN


def restaurant(df, default):
    assert len(default) == 3
    colname = R_to_col['Restaurant']
    data = np.array(df[colname])
    # Replace nan with default values
    for i in range(3):
        mask = data[:, i] == TOKEN.NA
        ic(f'{sum(mask)} rows have no {colname[i]}.')
        data[mask, i] = default[i]
    return data


if __name__ == '__main__':
    ic('Extracting data')
    path = 'Data/data.csv'
    df = pd.read_csv(path)
    df = df.fillna(TOKEN.NA)
    ic(type(['No Name', 'No Number', 'No Description']))
    restaurant(df, ['No Name', 'No Number', 'No Description'])
    # ic(type(df))
    # ic(list(df.loc[0]))
    # ic(list(df.columns))
