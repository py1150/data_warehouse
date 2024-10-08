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


## 1. Code Worfklow

The following sequence is necessary to execute the entire ETL:
1. 00_create_delete_resources.ipynb
2. create_tables.py
3. etl.py

### Main Codes

These codes have to be executed to construct carry out the entire ETL pipeline.

**00_create_delete_resources.ipynb**   
- this file contains a Jupyter notebook with cells to 
    - _set up_ and 
    - _delete_   
the required AWS ressources to <red>stop incurring AWS costs</red>.

- An IAM user with Administrator access is required (policy _AdministratorAccess_)
    - credentials have to be used for the connection to AWS to be able to create the ressources
- All ressources must be set up before the ETL worfklow can proceed
    - Specifically,    
    - 1. we create an IAM role with S3 read access (_dwhrole_) 
        - attach the policy: _AmazonS3ReadOnlyAccess_
    - 2. we create a Redshift Cluster
    - 3. open a TCP port to access the cluster endpoint (default vpc)
- Also, the notebook contains code to check the connection to the Redshift cluster once the steps above are completed                
- The notebook also contains code to delete
    - the Redshift Cluster
    - the IAM role

**etl.py**   
- loads configurations from _dwh.cfg_ (see below)
- loads _sql_queries.py_
- executes load staging tables
- inserts data from staging tables into the final tables

### Support Codes

These codes are called by the main codes described above.

**create_tables.py**  
- loads configurations from _dwh.cfg_  (see below)
- loads _sql_queries.py_  
- drops tables if they already exist 
- creates all tables with the defined schema

**dwh.cfg**
- **is not shared in this project due to confidentiality**
    - _Note:_ for illustration a skeleton of the file including the source data paths (S3) is contained in the respository as **dwh_blue.cfg**    
- contains all configurations necessary to
    - set up the AWS ressources (described above)
    - interact with the Redshift cluster

**sql_queries.py**    
- input to: create_tables, etl.py  
- loads configurations from _dwh.cfg_
- provides queries of the ETL
- Insertion
    - create a temporary staging tables
    - we insert into the final tables from the staging tables
    - we only select distinct rows
    - delete the staging table after we are done


## 2. Schema for Song Play Analysis

A description of the schema for final the tables of the database is outlined below. 

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
- if there is a choice, we try to assign the _smallest possible size_ to each column in order to
    - avoid excess capacities and other hand to     
    - allocate enough space to avoid insertion errors


Below all tables and columns are listed. If a data type out of the usual choice (i.e., _VARCHAR_ for character and _INTEGER_ for numeric) was used and/or a restriction was applied, the datatype/the restriction and a comment is noted next to the column name. For, the complete list of the assigned data types for every column, please refer to _sql_queries.py_ (create_table_queries). 



**Fact Table**
1. <corn>songplays</corn> - records in event data associated with song plays i.e. records with page ```NextSong```
    - _songplay_id_: we generate an index number; it should not be empty to identify the record --> integer with identity(0,1) NOT NULL
    - _start_time_: date with time information; it should not be empty to identify the record --> timestamp NOT NULL
        - _Note_ to obtain the information in timestamp format it needs to be converted from an integer format from the source. This was achieved as outlined in: https://docs.aws.amazon.com/redshift/latest/dg/r_Dateparts_for_datetime_functions.html (_for this and further references see section below_)
    - _user_id_
    - _level_: the number of characters is limited to 4 ASCII characters --> 4 bytes --> CHAR(4)
    - _song_id_: alphanumeric string with fixed length --> CHAR(18) 
    - _artist_id_: alphanumeric string with fixed length --> CHAR(18)
    - _session_id_: it should not be empty to identify the record; NOT NULL 
    - _location_
    - _user_agent_

**Dimension Tables**  

2. users - users in the app  
    - _user_id_  
    - _first_name_  
    - _last_name_  
    - _gender_: column contains one ASCII character --> 1 byte --> CHAR(1)  
    - _level_: (_see above_) 

3. songs - songs in music database  
    - _song_id_  
    - _title_
    - _artist_id_ (_see above_)
    - _year_
    - _duration_: decimal with 5 decimal places --> REAL  

4. artists - artists in music database
    - _artist_id_
    - _name_
    - _location_
    - _latitude_: decimal value with mulitple decimal places --> DOUBLE PRECISION
    - _longitude_: decimal value with mulitple decimal places --> DOUBLE PRECISION

5. time - timestamps of records in songplays broken down into specific units
    - _start_time_ (_see above_)
    - _hour_
    - _day_
    - _week_
    - _month_
    - _year_
    - _weekday_

## 3. Collection of Queries

### Example Analytical Query

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

### Management Queries
These queries are examples to check the content of the database.

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

- delete all rows in a table
```SQL
DELETE FROM songs;
```




## 4. References
**AWS Redshift Documentation**  
As a reference guide the AWS Redshift Documentation was used. In particular, the following ressources were used during the construction of the ETL:

https://docs.aws.amazon.com/redshift/latest/dg/c_Supported_data_types.html

https://docs.aws.amazon.com/redshift/latest/dg/r_DATE_PART_function.html

https://docs.aws.amazon.com/redshift/latest/dg/r_TO_TIMESTAMP.html

https://docs.aws.amazon.com/redshift/latest/dg/r_Dateparts_for_datetime_functions.html

https://docs.aws.amazon.com/redshift/latest/dg/r_STL_LOAD_ERRORS.html



