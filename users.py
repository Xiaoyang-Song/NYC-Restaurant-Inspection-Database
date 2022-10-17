from utils import *
from extract_data import *


def add_user(connection, account_name: str, passcode: str, dob='NULL', district='NULL'):
    dob_val = f"'{dob}'" if dob != 'NULL' else 'NULL'
    dis_val = f"'{district}'" if district != 'NULL' else 'NULL'
    if district != 'NULL':
        assert district in LOCATION_SET
    schema = f"Users(account_name, passcode, dob, district)"
    cmd = f"INSERT INTO {schema} VALUES('{account_name}', '{passcode}', {dob_val}, {dis_val})"
    cursor = connection.execute(cmd)


if __name__ == '__main__':
    ic('Users Manipulation Scripts')
