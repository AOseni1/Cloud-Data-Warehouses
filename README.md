**Project: Data Warehouse for Music Streaming Startup (Sparkify)**

Developed an ETL pipeline to migrate and transform data for Sparkify, a growing music streaming startup, onto Amazon Redshift for improved analytics. The project involved extracting user activity and song metadata stored as JSON logs in S3, staging the data in Redshift, and transforming it into a set of dimensional tables for easier analysis by the company's data team.

Key tasks:

- Designed and implemented an ETL pipeline to extract data from S3, load it into Redshift, and transform it into structured, query-optimized tables.
- Developed dimensional tables to support analytics on user behavior and song listening patterns.
- Streamlined data processing to ensure accurate and efficient querying for business insights.

This project demonstrated expertise in data engineering, cloud-based data storage (S3/Redshift), and ETL processes for supporting scalable data analysis.

STAGING TABLES

staging_events
artist
auth
firstName
gender
itemInSession
lastName
length
level
location
method
page
registration
sessionId
song
status
ts
userAgent
userId

staging_songs
song_id
num_songs
title
atist_name
artist_latitude
year
duration
artist_id
artist_longitude
artist_location

FACT TABLE

songplay_table
songplay_id PRIMARY KEY
start_time
user_id
level
song_id
artist_id
session_id
location
user_agent

DIMENSION TABLES

user_table
user_id PRIMARY KEY
first_name  
 last_name  
 gender  
 level

song_table
song_id PRIMARY KEY,
title  
 artist_id  
 year  
 duration

artist_table
artist_id PRIMARY KEY,
name  
 location  
 latitude  
 longitude

time_table
start_time PRIMARY KEY,
hour  
 day  
 week  
 month  
 year  
 weekday
