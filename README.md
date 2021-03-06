### Data Modeling in SQL/Relational Databases

This project discusses the data modeling in SQL using the data from Sparkify music app that contains the user event data and song information. 

The files description is given below:

1. data - This folder contains the user event and song information.
2. create_tables.py - This python file drops and creates the appropriate data tables to enter the data. You run this file to reset your tables before each time you run your ETL scripts.
3. sql_queries.py - This python file contains the SQL queries for the creation, insertion and selection needs for the data modelling. These are imported in the other files to execute.
4. test.ipynb - This Jupyter notebook is created to test the data inserted into the tables.
5. etl.ipynd - This Jupyter notebook will discuss the process of ETL to insert the data tables.
6. etl.py - This is the final python file that performs the ETL at one go. However, this will insert the record one after the other into the table.
7. etlX.py - This is the python file that performs ETL, with bulk insertion of data using copy_from() function in psycopg2.

#### About Data 

**Song Data** 

The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

song_data/A/B/C/TRABCEI128F424C983.json

song_data/A/A/B/TRAABJL12903CDCF1A.json

And below is an example of what a single song file, 

TRAABJL12903CDCF1A.json, looks like.

{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

**log Data** 

Log Dataset
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.

log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json

#### Data Modeling

Schema for Song Play Analysis:

Using the song and log datasets, you'll need to create a star schema optimized for queries on song play analysis. This includes the following tables.

Fact Table

songplays - records in log data associated with song plays i.e. records with page NextSong

songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

Dimension Tables

users - users in the app

user_id, first_name, last_name, gender, level

songs - songs in music database

song_id, title, artist_id, year, duration

artists - artists in music database

artist_id, name, location, latitude, longitude

time - timestamps of records in songplays broken down into specific units

start_time, hour, day, week, month, year, weekday
<div align='center'>
<img src="/images/schema.png" height="400" width="400">
</div>

**Importance of Fact and Dimension tables**

Fact tables capture the facts & measure of interests from the user log history by session, like which song is play at which moment, from which agent and location. While the Dimension tables store the additional information of the songs, artists, users, and time in separate tables. These additional knowledge can be obtained by joining the fact table with the appropriate dimension table. This reduces the data duplication in the one single table holding the entire information.

### How to use

1. Clone the repository
2. Run the PostgreSQL locally on 127.0.0.1
3. Everytime you need to create a new set of tables, run python create_tables.py MUST before going to etl.ipynb or etl.py.
4. Go through the etl.ipynb for the step by step explanation of ETL
5. Run etl.py or etlX.py to perform ETL for songs and logs data
6. Query the table using the queries in test.ipynb

### Tables:

**Songplays Table**

![songstable](/images/Songplays_table.png)

**Songs Table**

![songstable](/images/Songs_table.png)

**artist Table**

<img src="/images/artist_table.png" height="250" width="600">

<!-- ![artisttable]() -->

**users Table**

<img src="/images/users_table.png" height="200" width="400">

<!-- ![userstable]() -->

**Time Table**

<img src="/images/time_table.png" height="200" width="400">

<!-- ![timetable]() -->

