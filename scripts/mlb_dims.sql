use schema mlb;

-- person dimension table
create table if not exists dim_person (
    person_id string not null,
    first_name string,
    last_name string,
    primary key (person_id)
);
insert overwrite into dim_person
select
    id as person_id,
    first as first_name,
    last as last_name
from
    raw_data_snowsql.person_codes
;

-- park dimension table
create table if not exists dim_park (
    park_id string not null,
    name string,
    nickname string,
    city string,
    state string,
    notes string,
    primary key (park_id)
);
insert overwrite into dim_park
select
    park_id,
    name,
    aka as nickname,
    city,
    state,
    notes
from
    raw_data_snowsql.park_codes
;

-- league dimension table
create table if not exists dim_league (
    league_id string not null,
    name string,
    primary key (league_id)
);
insert overwrite into dim_league values
    ('NA', 'National Association'),
    ('NL', 'National League'),
    ('AA', 'American Association'),
    ('UA', 'Union Association'),
    ('PL', 'Players League'),
    ('AL', 'American League'),
    ('FL', 'Federal League')
;

-- appearance_type dimension table
create table if not exists dim_appearance_type (
    appearance_type_id string not null,
    name string,
    category string,
    primary key (appearance_type_id)
);
insert overwrite into dim_appearance_type
select
    appearance_type_id,
    name,
    category
from
    raw_data_snowsql.appearance_type
;

-- team dimension table
create table if not exists dim_team (
    team_id string not null,
    league_id string,
    city string,
    nickname string,
    franchise_id string,
    primary key (team_id),
    foreign key (league_id) references dim_league(league_id)
);
insert overwrite into dim_team
select
    team_id,
    league as league_id,
    city,
    nickname,
    franch_id as franchise_id
from
    raw_data_snowsql.team_codes
where
    team_id <> 'MIL' or (team_id = 'MIL' and end = 1997) -- this team has multiple records, only load most recent
;

-- game dimension table
create table if not exists dim_game (
    game_id string not null,
    date string,
    number_of_game string,
    park_id string,
    length_outs int,
    day boolean,
    completion string,
    forefeit string,
    protest string,
    attendance string,
    length_minutes int,
    additional_info string,
    acquisition_info string,
    primary key (game_id),
    foreign key (park_id) references dim_park(park_id)
);
insert overwrite into dim_game
select
    h_name || date || number_of_game as game_id,
    date,
    number_of_game,
    park_id,
    length_outs,
    case
        when day_night = 'D' then 1
        else 0
    end as day,
    completion,
    forefeit,
    protest,
    attendance,
    length_minutes,
    additional_info,
    acquisition_info
from
    raw_data_snowsql.game_log
;