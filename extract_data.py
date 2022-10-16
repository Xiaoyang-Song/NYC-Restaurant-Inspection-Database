from math import isnan
from icecream import ic
import pandas as pd
import numpy as np
from utils import R_to_col, TOKEN


def extract(df, num_fields: int, relation_name: str, default: list):
    assert len(default) == num_fields
    colname = R_to_col[relation_name]
    data = np.array(df[colname])
    # Replace NA with default values
    # for i in range(3):
    #     mask = data[:, i] == TOKEN.NA
    #     ic(f'{sum(mask)} rows have no {colname[i]}.')
    #     data[mask, i] = default[i]
    return data


def preprocess(path):
    df = pd.read_csv(path)
    # df = df.fillna(TOKEN.NA)
    # df = df.fillna()
    # Add more if needed
    return df


if __name__ == '__main__':
    ic('Extracting data')
    path = 'Data/data.csv'
    df = preprocess(path)
    restaurant = extract(df, 3, 'Restaurant', [
                         'No Name', 'No Number', 'No Description'])
    ic(restaurant[0, 2])
