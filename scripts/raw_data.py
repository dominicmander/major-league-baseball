import os
import pandas as pd

import data_types
import db_utils

def load_files(dir):
    """
    Loops through all files in specified directory and loads each file into
    a table of the same name
    """
    for file in os.scandir(dir):
        if file.is_file():
            path = file.path
            name = file.name.split('.')[0]
            dtypes_csv = data_types.data_types_csv[name]
            data = pd.read_csv(path, dtype=dtypes_csv)
            dtypes_sql = data_types.data_types_sql[name]
            db_utils.df_to_table(data, name, dtypes_sql)

if __name__ == '__main__':
    db_utils.db_engine('raw_data_python')
    load_files('../data/')
    # first run end to end took 00:24:14 with X-SMALL warehouse
    