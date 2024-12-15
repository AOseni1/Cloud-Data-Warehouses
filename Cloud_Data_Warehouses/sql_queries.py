import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

ARN = config.get("IAM_ROLE", "ARN")
LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS user_table;"
song_table_drop = "DROP TABLE IF EXISTS song_table;"
artist_table_drop = "DROP TABLE IF EXISTS artist_table;"
time_table_drop = "DROP TABLE IF EXISTS time_table;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
artist VARCHAR,
auth VARCHAR,
firstName VARCHAR,
gender CHAR(1),
itemInSession INT,
lastName VARCHAR,
length FLOAT,
level VARCHAR,
location VARCHAR,
method VARCHAR,
page VARCHAR,
registration INT,
sessionId INT,
song VARCHAR,
status INT,
ts INT,
userAgent VARCHAR,
userId INT
)
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
song_id VARCHAR,
num_songs INT,
title VARCHAR,
atist_name VARCHAR,
artist_latitude FLOAT,
year INT,
duration FLOAT,
artist_id VARCHAR,
artist_longitude FLOAT,
artist_location VARCHAR
)
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplay_table (
        songplay_id         INT         IDENTITY(0,1)   PRIMARY KEY,
        start_time          TIMESTAMP   NOT NULL,
        user_id             VARCHAR     NOT NULL,
        level               VARCHAR,
        song_id             VARCHAR     NOT NULL,
        artist_id           VARCHAR     NOT NULL,
        session_id          INT,
        location            VARCHAR,
        user_agent          VARCHAR
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS user_table (
        user_id             VARCHAR     PRIMARY KEY,
        first_name          VARCHAR,
        last_name           VARCHAR,
        gender              CHAR(1),
        level               VARCHAR
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS song_table (
        song_id             VARCHAR     PRIMARY KEY,
        title               VARCHAR,
        artist_id           VARCHAR     NOT NULL,
        year                INT,
        duration            FLOAT
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artist_table (
        artist_id           VARCHAR     PRIMARY KEY,
        name                VARCHAR,
        location            TEXT,
        latitude            FLOAT,
        longitude           FLOAT
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time_table (
        start_time          TIMESTAMP   PRIMARY KEY,
        hour                INT,
        day                 INT,
        week                INT,
        month               INT,
        year                INT,
        weekday             INT
    )
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_log_data from {}
CREDENTIALS {}
REGION 'us-west-2'
FORMAT AS JSON {}
""").format(config['S3']['LOG_DATA'],config['IAM_ROLE']['ARN'],config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
COPY staging_songs_data from {}
CREDENTIALS {}
REGION 'us-west-2'
JSON 'auto'
""").format(config['S3']['SONG_DATA'],config['IAM_ROLE']['ARN'])



# FINAL TABLES

songplay_table_insert = ("""
 INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT
        TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' AS start_time,
        se.userId       AS user_id,
        se.level,
        ss.song_id,
        ss.artist_id,
        se.sessionId    AS session_id,
        se.location,
        se.userAgent    AS user_agent
    FROM staging_events se
    JOIN staging_songs ss ON se.song = ss.title AND se.artist = ss.artist_name
    WHERE se.page = 'NextSong'
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT
        userId      AS user_id,
        firstName   AS first_name,
        lastName    AS last_name,
        gender,
        level
    FROM staging_events
    WHERE page = 'NextSong' AND userId IS NOT NULL
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
    WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT
        artist_id,
        artist_name         AS name,
        artist_location     AS location,
        artist_latitude     AS latitude,
        artist_longitude    AS longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT
        TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' AS start_time,
        EXTRACT(hour FROM start_time)       AS hour,
        EXTRACT(day FROM start_time)        AS day,
        EXTRACT(week FROM start_time)       AS week,
        EXTRACT(month FROM start_time)      AS month,
        EXTRACT(year FROM start_time)       AS year,
        EXTRACT(weekday FROM start_time)    AS weekday
    FROM staging_events
    WHERE ts IS NOT NULL
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
