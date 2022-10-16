from icecream import ic
import pandas as pd



def extract_cols(path):
    pass


if __name__ == '__main__':
    ic('Extracting data')
    path = 'Data/data.csv'
    df = pd.read_csv(path)
    ic(type(df))
    ic(list(df.loc[0]))
    ic(list(df.columns))
    ic(df[['GRADE', 'CAMIS']])