from utils import *
from extract_data import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy import *


def add_user(connection, uid, account_name: str, passcode: str, district='NULL'):
    # dob_val = f"'{dob}'" if dob != 'NULL' else 'NULL' # not need anymore
    dis_val = f"'{district}'" if district != 'NULL' else 'NULL'
    if district != 'NULL':
        assert district in LOCATION_SET
    schema = f"Users(userid, account_name, password, district)"
    try:
        # TODO: change this to avoid SQL injection
        cmd = f"INSERT INTO {schema} VALUES('{uid}', '{account_name}', '{passcode}', {dis_val})"
        cursor = connection.execute(cmd)
    except IntegrityError:
        error = f"User {uid} is already registered."
        return error
    else:
        return None


def add_feel(connection, uid, rid: list, feel: list):
    assert len(rid) == len(feel)
    for id, fl in zip(rid, feel):
        assert fl in FEEL_SET
        cmd = f"INSERT INTO Feel(userid, rid, feel) VALUES('{uid}', {id},'{fl}')"
        cursor = connection.execute(cmd)


def add_reviews(connection, uid: int, rid: int, content: str):
    # Errors relating to nonexisting rid and uid are handled elsewhere
    cmd = f"INSERT INTO Reviews_Post_Own(content, post_time, userid, rid) "\
          f"VALUES('{content}', '{get_time_signature()}', '{uid}', {rid})"
    cursor = connection.execute(cmd)


def del_feel(connection, uid, rid):
    cmd = "DELETE FROM Feel WHERE userid=(:uid) AND rid=(:rid)"
    connection.execute(text(cmd), uid=uid, rid=rid)


if __name__ == '__main__':
    ic('Users Manipulation Scripts')
