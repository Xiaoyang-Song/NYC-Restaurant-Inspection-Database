from enum import Enum
import pandas as pd
from icecream import ic
import numpy as np
from time import gmtime, strftime

R_to_col = {
    'Restaurant': ['DBA', 'PHONE', 'CUISINE DESCRIPTION'],
    'Location': ['BORO', 'BUILDING', 'STREET', 'ZIPCODE'],
    'Inspection': ['INSPECTION TYPE'],
    'Inspect': ['INSPECTION DATE'],
    'Violation': ['VIOLATION CODE', 'VIOLATION DESCRIPTION', 'CRITICAL FLAG'],
    'Grades': ['SCORE', 'GRADE'],
    'Graded': ['GRADE DATE']
}

RELATION_NAME = ['Restaurant']
LOCATION_SET = ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']
# NULL is added to handle edge case
GRADE_SET = ['A', 'B', 'C', 'P', 'N', 'Z', 'NULL']
FEEL_SET = ['Like', 'Dislike']

GRADE_DICT = {}
# Used for Web App Dev


class FL(Enum):
    LIKED, DISLIKED, IDLE = np.arange(3)


def get_time_signature():
    # return strftime("%m-%Y-%d-%H:%M:%S", gmtime()) # For specific time
    return strftime("%m/%d/%y", gmtime())


class TOKEN(Enum):
    NA = -1


if __name__ == '__main__':
    ic(R_to_col)
    ic(TOKEN.NA)
    ic(get_time_signature())
    ic(FL.IDLE.value == 2)
