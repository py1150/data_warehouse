<style>
    blue { color: blue }
    aqua { color: aqua }
    corn { color: cornflowerblue }
    red { color: red }
    green { color: chartreuse }
    yellow { color: yellow }
</style>

<green>
- 2024/03/27
    - create_tables.py: 
        - review data types - see Eagar(2023) p.278f  [x]
            - assign minimal storage size
        - update staging tales
            - use merge functionality
             --> this handles duplicates
                --> we use distinct                 [x]
    - AWS console
        - create new IAM user
        (with myRedshift role)
    - new codes
        - create redshift cluster
        - destroy redhisft cluster
</green>

# Data_warehouse
Udacity Nanodegree Data Engineering with AWS Project 2

## 0. Overview

The database... purpose....

## Project Overview / Workflow
- source data sets
- staging, final tables

- Execution:   
    - 0. set credentials / create redshift cluster
        at end we need
            - redshift cluster endpoint
            - IAM role ARN
        (create resources)
        we have to create
            - 0. create IAM user
            - 1. IAM role with S3 read access (myRedshiftRole) - might be there already
            - 2. Redshift Cluster
                --> code 2.1. to get status (including _endpoint_)
                --> code 2.2. to get cluster _endpoint and role ARN_ [there are 2 roles - IAM role see above and DWH role - here]
            - 3. tcp port to access the cluster endpoint (vpc)
            - 4. make sure you can connect
        (delete resources)
            - delete cluster
            - delete IAM role
    - 1. create_tables.py
    - 2. etl.py

    

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

Principles
- Star schema
- 2 major data types: character, numeric
- if there is a choice, we assign the smallest possible size
    - avoid excess capacities 
    - e.g., column gender is filled with 1 character with 1 byte ('F' or 'M') --> we can assign a fixed one-byte character: CHAR(1)
    - allocate enough space to avoid insertion errors

Insertion
- when inserting we 
    - create a temporary staging table
    - we insert into the final tables from the staging tables
    - we only select distinct rows
    - delete the staging table after we are done

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
    - gender: 1 ASCII character --> 1 byte
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

https://docs.aws.amazon.com/redshift/latest/dg/r_LPAD.html

https://docs.aws.amazon.com/redshift/latest/dg/r_CONCAT.html