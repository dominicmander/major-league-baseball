from configparser import SafeConfigParser
import os
import pandas as pd
from sqlalchemy import create_engine

import data_types

def db_config():
    parser = SafeConfigParser()
    parser.read('config.ini')
    db = dict(parser.items("keyrus_snowflake_db"))
    return db

def db_engine():
    engine = create_engine('snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}'.format(**db))
    return engine

def run_query(q):
    with engine.connect() as conn:
        return pd.read_sql(q, conn)

def run_command(c):
    with engine.connect() as conn:
        conn.execute(c)

def df_to_table(df, table, dtypes, exists='replace'):
    with engine.connect() as conn:
        df.to_sql(table, conn, dtype=dtypes, index=False, if_exists=exists, chunksize=10000)

def load_files(dir):
    for file in os.scandir(dir):
        if file.is_file():
            path = file.path
            name = file.name.split('.')[0]
            dtypes_csv = data_types.data_types_csv[name]
            data = pd.read_csv(path, dtype=dtypes_csv)
            dtypes_sql = data_types.data_types_sql[name]
            df_to_table(data, name, dtypes_sql)

if __name__ == '__main__':
    db = db_config()
    engine = db_engine()

    load_files('../data/')
    # first run end to end took 00:24:14 with X-SMALL warehouse
    