from configparser import SafeConfigParser
from sqlalchemy import create_engine
import pandas as pd

def db_engine(schema):
    parser = SafeConfigParser()
    parser.read('config.ini')
    db = dict(parser.items("keyrus_snowflake_db"))
    db['schema'] = schema

    global engine
    engine = create_engine('snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}'.format(**db))

def run_query(q):
    try:
        with engine.begin() as conn:
            return pd.read_sql(q, conn)
    except NameError:
        print("no engine defined, use db_utils.db_engine(schema) to define")

def run_command(c):
    try:
        with engine.begin() as conn:
            conn.execute(c)
    except NameError:
        print("no engine defined, use db_utils.db_engine(schema) to define")

def df_to_table(df, table, dtypes, exists='replace'):
    try:
        with engine.begin() as conn:
            df.to_sql(table, conn, dtype=dtypes, index=False, if_exists=exists, chunksize=10000)
    except NameError:
        print("no engine defined, use db_utils.db_engine(schema) to define")
