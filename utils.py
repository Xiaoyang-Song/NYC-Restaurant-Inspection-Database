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


class TOKEN(Enum):
    NA = np.arange(1)


if __name__ == '__main__':
    ic(R_to_col)
    ic(TOKEN.NA)
