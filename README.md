# Major League Baseball

## Setup

1. Install snowsql (see [docs](https://docs.snowflake.net/manuals/user-guide/snowsql-install-config.html]))
1. Run `chmod 700 ~/.snowsql/config` to secure
1. In `~/.snowsql/config` under `[connections]` configure default `accountname`, `username` and `password`
1. In `~/.snowsql/config` under `[variables]` create `mlb_s3_bucket_url`, `mlb_aws_key_id` and `mlb_aws_secret_key` variables
1. Run `snowsql -f setup.sql` to create database, warehouse, schema, stage etc
1. In `~/.snowsql/config` create new connection `[connections.mlb]` with `accountname`, `username`, `password`, `dbname` and `warehousename`
1. In `script` folder create `config.ini` using `sample_config.ini` as template (you can then use `snowsql -c <snowflake_connection_name>` to connect easily in future)

## Usage

 * `setup.sql` creates database, warehouse, schema, stage etc
 * `raw_data.sql` creates tables and populates data in raw_data_snowsql schema
 * optional `raw_data.py` creates tables and populates data in raw_data_python schema (for comparison)
 * `mlb_dims.sql` creates dimension tables and populates data
 * `mlb_facts.sql` creates fact tables and populates some data
 * `appearance_person.py` populates remaining fact data
 * `snowpipe.sql` creates table and pipe for snowpipe
 * `snowpipe_basic.py` basic sample snowpipe ingestion request

## Other scripts

 * `setup_utils.py` core setup utility functions e.g. logging
 * `data_types.py` dictionaries containing data types for `raw_data.py`
 * `ad_hoc/` ad hoc scripts that may be useful for future reference

## Data

Major League Baseball data from retrosheet - https://www.retrosheet.org/gamelogs/index.html
