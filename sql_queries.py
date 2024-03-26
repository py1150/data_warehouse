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
    CREATE TABLE staging_events (\
        artist VARCHAR(200),\
        auth VARCHAR(20),\
        firstName VARCHAR(50),\
        gender VARCHAR(5),\
        itemInSession INTEGER,\
        lastName VARCHAR(50),\
        length DOUBLE PRECISION,\
        level VARCHAR(200),\
        location VARCHAR(100),\
        method VARCHAR(10),\
        page VARCHAR(200),\
        registration DOUBLE PRECISION,\
        sessionID INTEGER,\
        song VARCHAR(200),\
        status INTEGER,\
        ts INTEGER,\
        userAgent VARCHAR(100),\
        userID INTEGER\
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE staging_songs (\
        num_songs INTEGER,\
        artist_id VARCHAR(50),\
        artist_latitude DOUBLE PRECISION,\
        artist_longitude DOUBLE PRECISION,\
        artist_location VARCHAR(100),\
        artist_name VARCHAR(100),\
        song_id VARCHAR(50),\
        title VARCHAR(200),\
        duration VARCHAR(50),\
        year INTEGER\
    );
""")

   

songplay_table_create = ("""
    CREATE TABLE songplays (\
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
    CREATE TABLE users (\
        user_id INTEGER NOT NULL,\
        first_name VARCHAR(50) NOT NULL,\
        last_name VARCHAR(50) NOT NULL,\
        gender VARCHAR(5) NOT NULL,\                     
        level VARCHAR(20) NOT NULL
    );
""")

song_table_create = ("""
    CREATE TABLE songs (\
        song_id VARCHAR(50) NOT NULL,\
        title VARCHAR(200) NOT NULL,\
        artist_id VARCHAR(50) NOT NULL,\
        year INTEGER NOT NULL,\            
        duration DOUBLE PRECISION NOT NULL
    );
""")

artist_table_create = ("""
    CREATE TABLE artists (\
        artist_id VARCHAR(50) NOT NULL,\
        name VARCHAR(100) NOT NULL,\
        location VARCHAR(100),\
        latitude DOUBLE PRECISION,\
        longitude DOUBLE PRECISION
    );
""")

time_table_create = ("""
    CREATE TABLE time (\
        start_time TIMESTAMP NOT NULL,\
        hour INTEGER NOT NULL,\
        day INTEGER NOT NULL,\
        week INTEGER NOT NULL,\
        month INTEGER NOT NULL,\
        year INTEGER NOT NULL,\
        weekday INTEGER NOT NULL\        
    );
""")

# STAGING TABLES


staging_events_copy = ("""
    copy sporting_event_ticket from 's3://udacity-dend/log_data'
    credentials 'aws_iam_role={}'
    gzip delimiter ';' compupdate off region 'us-west-2';
    format as JSON 's3://udacity-dend/log_json_path.json';
""").format(DWH_ROLE_ARN)

staging_songs_copy = ("""
    copy sporting_event_ticket from 's3://udacity-dend/song_data'
    credentials 'aws_iam_role={}'
    gzip delimiter ';' compupdate off region 'us-west-2';
""").format(DWH_ROLE_ARN)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)\
    SELECT\
        events.songplay_id,\
        CONCAT(LPAD(TO_CHAR(events.userID),4,'0'), CONCAT( LPAD(TO_CHAR(events.sessionID),5,'0'), LPAD(TO_CHAR(events.itemInSession),3,'0'))),\
        TO_TIMESTAMP(events.ts, 'YYYY-MM-DD HH24:MI:SS'),\
        events.user_id,\
        events.level,\
        songs.song_id,\
        songs.artist_id,\
        events.session_id,\
        events.location,\
        events.user_agent\
    FROM staging_events as events\
    JOIN staging_songs as songs\
        on
    ;\
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)\
    SELECT\
        user_id,\
        firstName,\
        lastName,\
        gender,\
        level\
    FROM staging_events\
""")

song_table_insert = ("""
    INSERT INTO song (song_id,title,artist_id,year, duration)\
    SELECT\
        song_id,\
        title,\
        artist_id,\
        year,\
        duration\
    FROM staging_songs\
    ;
""")

artist_table_insert = ("""
    INSERT INTO artist (artist_id,name,location,latitude,longitude)\
    SELECT\
        artist_id,\
        artist_name,\
        artist_location,\
        artist_latitude,\
        artist_longitude\
    FROM staging_songs\
    ;
""")

time_table_insert = ("""
    INSERT INTO time (start_time,hour,day,week,month,year,weekday)\
    SELECT\
        TO_TIMESTAMP(ts, 'YYYY-MM-DD HH24:MI:SS'),\
        DATE_PART(hour,TO_TIMESTAMP(ts, 'YYYY-MM-DD HH24:MI:SS')),\
        DATE_PART(day,TO_TIMESTAMP(ts, 'YYYY-MM-DD HH24:MI:SS')),\
        DATE_PART(week,TO_TIMESTAMP(ts, 'YYYY-MM-DD HH24:MI:SS')),\
        DATE_PART(month,TO_TIMESTAMP(ts, 'YYYY-MM-DD HH24:MI:SS')),\
        DATE_PART(year,TO_TIMESTAMP(ts, 'YYYY-MM-DD HH24:MI:SS')),\
        DATE_PART(dayofweek,TO_TIMESTAMP(ts, 'YYYY-MM-DD HH24:MI:SS')),\
    FROM staging_events\
    ;
""")



# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
