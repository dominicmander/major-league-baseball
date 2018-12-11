
--create db
create database if not exists mlb
    comment = 'major league baseball statistics'
;
use database mlb;

--create schemas
create schema if not exists raw_data_python
    comment = 'raw data loaded in python'
;
create schema if not exists raw_data_snowsql
    comment = 'raw data loaded in snowsql'
;
create schema if not exists mlb
    comment = 'core mlb data'
;

--create wh
create or replace warehouse mlb_wh with
    warehouse_size = 'X-SMALL'
    auto_suspend = 180
    auto_resume = true
    initially_suspended = true
    comment = 'warehouse for working with mlb database'
;

--prepare raw_data_snowsql schema
    use schema raw_data_snowsql;

    --create file format
    create or replace file format mlb_csv
        type = csv
        skip_header = 1
        field_optionally_enclosed_by = '"'
    ;

    --create stage
    create or replace stage mlb_stage
        url = '&mlb_s3_bucket_url'
        credentials = (aws_key_id='&mlb_aws_key_id' aws_secret_key='&mlb_aws_secret_key')
        file_format = mlb_csv
    ;

    --list staged files
    list @mlb_stage;