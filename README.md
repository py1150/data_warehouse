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
Sparkify is a music stream startup. They want to move their song database and their proceses to the cloud.

Their analytic target is to understand which songs their users are listening to.

For this purpose we constructed a cloud-based ETL pipeline which extracts data from AWS S3, loads them into staging tables in AWS Redshift and transforms the data into final tables which can be used as the bassi for anylsis.

The details of the ETL pipeline outlined below, specifically:
- its workflow
- the data schema
- example queries for troubleshooting and analytic purposes.

## Project Overview / Workflow
- source data sets
- staging, final tables

- Execution:   
- 0. setup ressources
    - 0.1. Create an IAM User with Administrative permissions
        - Attach Policy _AdministratorAccess_
        - needed to perform AWS operations outlined below (e.g., create a new IAM Role)
        --> store credentials in dwh.cfg
    - 0.2. Create Ressources
        at end we need
            - redshift cluster endpoint
            - IAM role ARN
        (create resources)
        we have to create
            - 0. create IAM user with Administrator access (see above)
            - 1. IAM role with S3 read access (_dwhrole_) - might be there already
                - specifically, we
                    - create the role
                    - attach the policy: _AmazonS3ReadOnlyAccess_
                - --> creating the IAM Role renders the IAM role ARN
                - --> we have to add it to _dwh.cfg_
                - Output:
                ```PYTHON
                1.1 Creating a new IAM Role
                1.2 Attaching Policy
                1.3 Get the IAM role ARN
                arn:aws:iam::137423019814:role/dwhRole
                ```
            - 2. Redshift Cluster
                - password is defined in dwh.cfg
                    - must be at least 8 characters long
                --> code 2.1. to get status (including _endpoint_)
                --> code 2.2. to get cluster _endpoint and role ARN_ [there are 2 roles - IAM role see above and DWH role - here]
            - 3. tcp port to access the cluster endpoint (vpc)
                - sg id: ```sg-0c365fc55381dced9```
            - 4. check connection
                - connection successful:
                ```
                postgresql://dwhprojectuser:$rtZ5l47@dwhcluster.cx4heaylzzsk.us-west-2.redshift.amazonaws.com:5439/dwh

                'Connected: dwhprojectuser@dwh'
                ```
        (delete resources)
            - delete cluster
            - delete IAM role
    - 1. create_tables.py
        - check schema with _Query Editor_ (AWS Redshift console)
    - 2. etl.py

- Load Tables
    - for testing purposes performed with a subset
- Insert
    - Time format see https://docs.aws.amazon.com/redshift/latest/dg/r_Dateparts_for_datetime_functions.html

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

A description of the schema for the tables of the database is outlined below. 

For constructing the schema we followed the following principles:  
**Schema**
- the tables are aligned in a _star schema_ in order to:
    - enable an organization which is intuitive for the business users when they try to answer their analytical questions  

**Data Types**  
- we use 3 major data types: 
    - _character_
    - _numeric_
    - _timestamp_ 
- On the specific data types on column level, please read below
- if there is a choice, we assign the _smallest possible size_ to each column in order to
    - avoid excess capacities and other hand to     
    - allocate enough space to avoid insertion errors


Below all tables and columns are listed. If a data type out of the usual choice (i.e., _VARCHAR_ for character and _INTEGER_ for numeric) was used, the datatype and a comment is noted next to the column name. For, the complete list of the assigned data types for every column, please refer to _sql_queries.py_ (create_table_queries). 


- e.g., column gender is filled with 1 character with 1 byte ('F' or 'M') --> we can assign a fixed one-byte character: CHAR(1)

Insertion
- when inserting we 
    - create a temporary staging table
    - we insert into the final tables from the staging tables
    - we only select distinct rows
    [- delete the staging table after we are done]

**Fact Table**
1. <corn>songplays</corn> - records in event data associated with song plays i.e. records with page ```NextSong```
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



## Management Queries

- check load error
```SQL
select 	
    starttime, filename, err_reason, colname, type, col_length, position, raw_field_value
from stl_load_errors
order by starttime desc
; 
```

- check content of tables
```SQL
SELECT * FROM staging_events limit 10;
SELECT * FROM staging_songs limit 10;
SELECT * FROM songplays limit 10;
SELECT * FROM songs;
```

```SQL
DELETE FROM songs;
```

## Example Analytical Query

The query below is an example of the information which could be retrieved by business users from the database. The example below is also contained in _etl.py_.

- most played song on sunday
   
```SQL
/*most played song on sunday*/
select
	a.song_id
    ,songs.title
from (
    select 
            song_id
            ,count(*) as n
    from songplays
    where DATEPART(day, start_time)=7
    group by song_id
    order by count(*) desc
    limit 1
  	) as a
left join songs
	on a.song_id=songs.song_id
;
```


## References
**AWS Redshift Documentation**
As a reference guide the AWS Redshift Documentation was used. In particular, the following ressources were used during the construction of the ETL:

https://docs.aws.amazon.com/redshift/latest/dg/c_Supported_data_types.html

https://docs.aws.amazon.com/redshift/latest/dg/r_DATE_PART_function.html

https://docs.aws.amazon.com/redshift/latest/dg/r_TO_TIMESTAMP.html

https://docs.aws.amazon.com/redshift/latest/dg/r_Dateparts_for_datetime_functions.html

https://docs.aws.amazon.com/redshift/latest/dg/r_STL_LOAD_ERRORS.html



