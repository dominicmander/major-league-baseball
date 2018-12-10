use schema mlb;

-- appearance_team fact table
create table if not exists fact_appearance_team (
    team_id string not null,
    game_id string not null,
    home boolean,
    league_id string,
    score int,
    line_score string,
    at_bats int,
    hits int,
    doubles int,
    triples int,
    homeruns int,
    rbi int,
    sacrifice_hits int,
    sacrifice_flies int,
    hit_by_pitch int,
    walks int,
    intentional_walks int,
    strikeouts int,
    stolen_bases int,
    caught_stealing int,
    grounded_into_double int,
    first_catcher_interference int,
    left_on_base int,
    pitchers_used int,
    individual_earned_runs int,
    team_earned_runs int,
    wild_pitches int,
    balks int,
    putouts int,
    assists int,
    errors int,
    passed_balls int,
    double_plays int,
    triple_plays int,
    primary key (team_id, game_id),
    foreign key (team_id) references dim_team(team_id),
    foreign key (game_id) references dim_game(game_id),
    foreign key (league_id) references dim_league(league_id)
);
insert overwrite into fact_appearance_team
select
    h_name                              as team_id,
    game_id                             ,
    1                                   as home,
    h_league                            as league_id,
    h_score                             as score,
    h_line_score                        as line_score,
    h_at_bats                           as at_bats,
    h_hits                              as hits,
    h_doubles                           as doubles,
    h_triples                           as triples,
    h_homeruns                          as homeruns,
    h_rbi                               as rbi,
    h_sacrifice_hits                    as sacrifice_hits,
    h_sacrifice_flies                   as sacrifice_flies,
    h_hit_by_pitch                      as hit_by_pitch,
    h_walks                             as walks,
    h_intentional_walks                 as intentional_walks,
    h_strikeouts                        as strikeouts,
    h_stolen_bases                      as stolen_bases,
    h_caught_stealing                   as caught_stealing,
    h_grounded_into_double              as grounded_into_double,
    h_first_catcher_interference        as first_catcher_interference,
    h_left_on_base                      as left_on_base,
    h_pitchers_used                     as pitchers_used,
    h_individual_earned_runs            as individual_earned_runs,
    h_team_earned_runs                  as team_earned_runs,
    h_wild_pitches                      as wild_pitches,
    h_balks                             as balks,
    h_putouts                           as putouts,
    h_assists                           as assists,
    h_errors                            as errors,
    h_passed_balls                      as passed_balls,
    h_double_plays                      as double_plays,
    h_triple_plays                      as triple_plays
from
    raw_data_snowsql.game_log
union
select
    v_name                              as team_id,
    game_id                             ,
    0                                   as home,
    v_league                            as league_id,
    v_score                             as score,
    v_line_score                        as line_score,
    v_at_bats                           as at_bats,
    v_hits                              as hits,
    v_doubles                           as doubles,
    v_triples                           as triples,
    v_homeruns                          as homeruns,
    v_rbi                               as rbi,
    v_sacrifice_hits                    as sacrifice_hits,
    v_sacrifice_flies                   as sacrifice_flies,
    v_hit_by_pitch                      as hit_by_pitch,
    v_walks                             as walks,
    v_intentional_walks                 as intentional_walks,
    v_strikeouts                        as strikeouts,
    v_stolen_bases                      as stolen_bases,
    v_caught_stealing                   as caught_stealing,
    v_grounded_into_double              as grounded_into_double,
    v_first_catcher_interference        as first_catcher_interference,
    v_left_on_base                      as left_on_base,
    v_pitchers_used                     as pitchers_used,
    v_individual_earned_runs            as individual_earned_runs,
    v_team_earned_runs                  as team_earned_runs,
    v_wild_pitches                      as wild_pitches,
    v_balks                             as balks,
    v_putouts                           as putouts,
    v_assists                           as assists,
    v_errors                            as errors,
    v_passed_balls                      as passed_balls,
    v_double_plays                      as double_plays,
    v_triple_plays                      as triple_plays
from
    raw_data_snowsql.game_log
;

-- appearance_person fact table
create table if not exists fact_appearance_person (
    appearance_id int autoincrement,
    person_id string,
    team_id string,
    game_id string,
    appearance_type_id string,
    primary key (appearance_id),
    foreign key (person_id) references dim_person(person_id),
    foreign key (team_id) references dim_team(team_id),
    foreign key (game_id) references dim_game(game_id),
    foreign key (appearance_type_id) references dim_appearance_type(appearance_type_id)
);
-- table is populated by appearance_person.py