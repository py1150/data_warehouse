import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_events;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS user"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
""")

staging_songs_table_create = ("""
""")

   

songplay_table_create = ("""
    CREATE TABLE songplays (
        songplay_id INTEGER NOT NULL,\
        start_time TIMESTAMP NOT NULL,\
        user_id  INTEGER NOT NULL,\
        level VARCHAR(20) NOT NULL,\
        song_id VARCHAR(50) NOT NULL,\
        artist_id VARCHAR(50) NOT NULL,\
        session_id INTEGER NOT NULL,\
        location VARCHAR(100) NOT NULL,\
        user_agent VARCHAR(100) NOT NULL\
    );
""")

user_table_create = ("""
    CREATE TABLE users (
        user_id INTEGER NOT NULL,\
        first_name VARCHAR(50) NOT NULL,\
        last_name VARCHAR(50) NOT NULL,\
        gender VARCHAR(5) NOT NULL,\                     
        level VARCHAR(20) NOT NULL
    );
""")

song_table_create = ("""
    CREATE TABLE songs (
        song_id VARCHAR(50) NOT NULL,\
        title VARCHAR(200) NOT NULL,\
        artist_id VARCHAR(50) NOT NULL,\
        year INTEGER NOT NULL,\            
        duration DOUBLE PRECISION NOT NULL
    );
""")

artist_table_create = ("""
""")

time_table_create = ("""
""")

# STAGING TABLES

json mapping must be inserted
%%time
qry = """
    copy sporting_event_ticket from 's3://udacity-labs/tickets/split/part'
    credentials 'aws_iam_role={}'
    gzip delimiter ';' compupdate off region 'us-west-2';
""".format(DWH_ROLE_ARN)

%sql $qry

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
