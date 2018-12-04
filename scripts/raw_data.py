from configparser import SafeConfigParser
import pandas as pd
from sqlalchemy import create_engine

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

def df_to_table(df, table, exists='fail'):
    with engine.connect() as conn:
        df.to_sql(table, conn, index=False, if_exists=exists, chunksize=10000)

if __name__ == '__main__':
    db = db_config()
    engine = db_engine()
    
    person_codes = pd.read_csv('../data/person_codes.csv')
    df_to_table(person_codes, 'person_codes')
    