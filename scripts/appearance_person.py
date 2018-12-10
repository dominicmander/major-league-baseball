import db_utils

# prepare database engine
db_utils.db_engine('mlb')

# template query for populating non-player person appearances
c_pop_appearance_person_non_players_template = """
    INSERT INTO fact_appearance_person (
        game_id,
        team_id,
        person_id,
        appearance_type_id
    )
        SELECT
            game_id,
            {team},
            {field},
            {appearance_type}
        FROM
            raw_data_snowsql.game_log
        WHERE
            {field} IS NOT NULL
    ;
    """

# list of query parameters for non-player person appearance types
c_pop_appearance_person_non_players_queries = [
    ["hp_umpire_id", "'UHP'", "NULL"],
    ["fb_umpire_id", "'U1B'", "NULL"],
    ["sb_umpire_id", "'U2B'", "NULL"],
    ["tb_umpire_id", "'U3B'", "NULL"],
    ["lf_umpire_id", "'ULF'", "NULL"],
    ["rf_umpire_id", "'URF'", "NULL"],
    ["v_manager_id", "'MM'", "v_name"],
    ["h_manager_id", "'MM'", "h_name"],
    ["winning_pitcher_id", "'AWP'", "NULL"],
    ["losing_pitcher_id", "'ALP'", "NULL"],
    ["saving_pitcher_id", "'ASP'", "NULL"],
    ["winning_rbi_batter_id", "'AWB'", "NULL"],
    ["v_starting_pitcher_id", "'PSP'", "v_name"],
    ["h_starting_pitcher_id", "'PSP'", "h_name"]
]

# truncate existing table and re-create primary key (to reset autoincrement)
db_utils.run_command("TRUNCATE TABLE fact_appearance_person;")
db_utils.run_command("ALTER TABLE fact_appearance_person DROP COLUMN appearance_id;")
db_utils.run_command("ALTER TABLE fact_appearance_person ADD COLUMN appearance_id INT AUTOINCREMENT PRIMARY KEY;")

# for each set of parameters run query
for query in c_pop_appearance_person_non_players_queries:
    query_vars = {
        'field': query[0],
        'appearance_type': query[1],
        'team': query[2]
    }
    db_utils.run_command(c_pop_appearance_person_non_players_template.format(**query_vars))

# template query for populating player appearances
c_pop_appearance_person_players_template = """
    INSERT INTO fact_appearance_person (
        game_id,
        team_id,
        person_id,
        appearance_type_id
    ) 
        SELECT
            game_id,
            {hv}_name,
            {hv}_player_{num}_id,
            'O{num}'
        FROM
            raw_data_snowsql.game_log
        WHERE
            {hv}_player_{num}_id IS NOT NULL

    UNION

        SELECT
            h_name || date || number_of_game,
            {hv}_name,
            {hv}_player_{num}_id,
            'D' || CAST({hv}_player_{num}_def_pos AS INT)
        FROM
            raw_data_snowsql.game_log
        WHERE
            {hv}_player_{num}_id IS NOT NULL
    ;
    """

# for each player number (h 1-10 and v 1-10) run query
for hv in ['h','v']:
    for num in range(1,10):
        query_vars = {
            "hv": hv,
            "num": num
        }
        db_utils.run_command(c_pop_appearance_person_players_template.format(**query_vars))
