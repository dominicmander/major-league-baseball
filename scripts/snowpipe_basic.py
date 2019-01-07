import logging
from configparser import SafeConfigParser
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from snowflake.ingest import SimpleIngestManager
from snowflake.ingest import StagedFile
from snowflake.ingest.error import IngestResponseError
import time
import datetime
from requests import HTTPError

import setup_utils

# prepare logging
logger = logging.getLogger()
setup_utils.setup_logging(logger)
log = logging.getLogger(__name__)

# load config
# contains user, keypassphrase, account, host and pipe attributes
parser = SafeConfigParser()
parser.read('config.ini')
pipe = dict(parser.items("keyrus_snowflake_pipe"))

# add private key to dictionary (and drop keypassphrase)
with open('/home/dom/.ssh/sys_mlb_snowpipe_key.p8', 'rb') as key:
    pipe['private_key'] = load_pem_private_key(
        key.read(),
        password=pipe.pop('keypassphrase').encode(),
        backend=default_backend()
    )

# ingest manager
ingest_manager = SimpleIngestManager(**pipe)

# list of files to ingest
file_list = ['game_log_2017_04.csv']
staged_file_list = []
for file_name in file_list:
    staged_file_list.append(StagedFile(file_name, None))

# submit ingestion request
try:
    resp = ingest_manager.ingest_files(staged_file_list)
    log.info(f"Ingest Manager Response: {resp['responseCode']}")
except (IngestResponseError, HTTPError) as e:
    log.error(e)
    exit(1)

# check ingestion resulted in 'SUCCESS' response
assert(resp['responseCode'] == 'SUCCESS')

# wait for ingestion history
while True:
    expected_files = len(file_list)
    history_resp = ingest_manager.get_history()

    if len(history_resp['files']) == expected_files:
        log.info(f"Ingest Report:\n{history_resp}")
        break
    else:
        log.info("waiting 20 seconds")
        time.sleep(20)

# get ingestion history for time range
# Valid ISO 8601 format requires Z at the end
hour = datetime.timedelta(hours=1)
date = datetime.datetime.utcnow() - hour
history_range_resp = ingest_manager.get_history_range(date.isoformat() + 'Z')

log.info(f"History Scan Report:\n{history_range_resp}")
