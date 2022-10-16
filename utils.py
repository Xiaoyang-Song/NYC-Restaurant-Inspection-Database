import pandas as pd
from icecream import ic

R_to_col = {
    'Restaurant': ['DBA', 'PHONE', 'CUISINE DESCRIPTION'],
    'Location': ['BORO', 'BUILDING', 'STREET', 'ZIPCODE'],
    'Inspection': ['INSPECTION TYPE'],
    'Inspect': ['INSPECTION DATE'],
    'Violation': ['VIOLATION CODE', 'VIOLATION DESCRIPTION', 'CRITICAL FLAG'],
    'Grades': ['SCORE', 'GRADE'],
    'Graded': ['GRADE DATE']
}

if __name__ == '__main__':
    ic(R_to_col)
