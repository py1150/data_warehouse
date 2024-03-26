<style>
    blue { color: blue }
    aqua { color: aqua }
    corn { color: cornflowerblue }
    red { color: red }
    green { color: chartreuse }
    yellow { color: yellow }
</style>

# Data_warehouse
Udacity Nanodegree Data Engineering with AWS Project 2

## 0. Overview

The database... purpose....

## Project Overview / Workflow
- source data sets
- staging, final tables

## 1. Code Worfklow
**etl.py**   
- loads configurations from _dwh.cfg_
- loads sql_queries.py
- executes load staging tables
- inserts 


**create_tables.py**  
- loads configurations from _dwh.cfg_  
- loads sql_queries.py  
- drops tables  
- creates tables  

**dwh.cfg**
HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=


**sql_queries.py**    
- input to: etl.py  
- loads configurations from _dwh.cfg_
- provides a list of queries

- create_table_queries
- drop_table_ queries
- copy_table_queries  
- insert_table_queries  

## 2. Schema for Song Play Analysis

Star schema

**Fact Table**
1. songplays - records in event data associated with song plays i.e. records with page ```NextSong```
    - songplay_id
    - start_time
    - user_id
    - level
    - song_id 
    - artist_id
    - session_id 
    - location
    - user_agent

**Dimension Tables**
2. users - users in the app
    - user_id
    - first_name
    - last_name
    - gender
    - level
3. songs - songs in music database
    - song_id
    - title
    - artist_id
    - year
    - duration
4. artists - artists in music database
    - artist_id
    - name
    - location
    - latitude
    - longitude
5. time - timestamps of records in songplays broken down into specific units
    - start_time
    - hour
    - day
    - week
    - month
    - year
    - weekday




## . Example Queries

## References
- AWS Redshift Documentation

https://docs.aws.amazon.com/redshift/latest/dg/r_DATE_PART_function.html

https://docs.aws.amazon.com/redshift/latest/dg/r_TO_TIMESTAMP.html