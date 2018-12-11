import logging
from configparser import SafeConfigParser
from sqlalchemy import create_engine
import pandas as pd

import setup_utils

# prepare logging
log = logging.getLogger(__name__)
setup_utils.setup_logging(log)

def db_engine(schema):
    """
    create sqlalchemy engine using config.ini for specified schema
    """
    parser = SafeConfigParser()
    parser.read('config.ini')
    db = dict(parser.items("keyrus_snowflake_db"))
    db['schema'] = schema

    global engine
    log.info(f"creating snowflake engine: #{db['warehouse']}@{db['database']}.{schema}")
    engine = create_engine('snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}'.format(**db))
    log.debug("engine created")

def run_query(q):
    """
    run specified sql query using previously created engine and return df
    """
    try:
        with engine.begin() as conn:
            q_log = ' '.join(q.split())[:50]
            log.info(f"executing query: {q_log}")
            result = pd.read_sql(q, conn)
            log.debug("execution done")
            return result
    except NameError:
        log.warn("no engine defined, use db_utils.db_engine(schema) to define")

def run_command(c):
    """
    run specified sql command using previously created engine
    """
    try:
        with engine.begin() as conn:
            c_log = ' '.join(c.split())[:50]
            log.info(f"executing command: {c_log}")
            conn.execute(c)
            log.debug("execution done")
    except NameError:
        log.warn("no engine defined, use db_utils.db_engine(schema) to define")

def df_to_table(df, table, dtypes, exists='replace'):
    """
    create table from specified dataframe

    arguments:
    df -- source dataframe
    table -- target table (will be created if doesn't exist)
    dtypes -- dictionary specifying desired datatypes
    exists -- behaviour if target table already exists (default replace)
    """
    try:
        with engine.begin() as conn:
            log.info(f"creating/replacing table: {table}")
            df.to_sql(table, conn, dtype=dtypes, index=False, if_exists=exists, chunksize=10000)
            log.debug("execution done")
    except NameError:
        log.warn("no engine defined, use db_utils.db_engine(schema) to define")
