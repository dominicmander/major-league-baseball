use role accountadmin;

--create role
create or replace role mlb_snowpipe
    comment = 'MLB snowpipe role'
;

--set up role hierarchy
grant role mlb_snowpipe to role sysadmin;

--grant privileges to role
grant usage             on database mlb                                 to role mlb_snowpipe;
grant usage             on schema mlb.raw_data_snowpipe                 to role mlb_snowpipe;
grant insert, select    on table mlb.raw_data_snowpipe.game_log         to role mlb_snowpipe;
grant usage             on stage mlb.raw_data_snowpipe.mlb_snowpipe     to role mlb_snowpipe;
grant usage             on file format mlb.raw_data_snowpipe.mlb_txt    to role mlb_snowpipe;

--grant ownership of pipe to role
use database mlb;
use schema raw_data_snowpipe;
alter pipe game_log set pipe_execution_paused = true;
grant ownership on pipe mlb.raw_data_snowpipe.game_log to role mlb_snowpipe;
select system$pipe_force_resume('game_log');

--create user
create or replace user sys_mlb_snowpipe
    default_role = mlb_snowpipe
    comment = 'System user for MLB snowpipe'
;

--create public/private key pair
--openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out sys_mlb_snowpipe_key.p8
--openssl rsa -in sys_mlb_snowpipe_key.p8 -pubout -out sys_mlb_snowpipe_key.pub

--assign key to user
--alter user sys_mlb_snowpipe set rsa_public_key='<public key>';
