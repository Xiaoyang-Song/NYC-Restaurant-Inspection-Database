from enum import Enum
import pandas as pd
from icecream import ic
import numpy as np

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
GRADE_SET = ['A', 'B', 'C', 'P', 'N', 'Z', 'NULL'] # NULL is added to handle edge case

class TOKEN(Enum):
    NA = -1


if __name__ == '__main__':
    ic(R_to_col)
    ic(TOKEN.NA)
