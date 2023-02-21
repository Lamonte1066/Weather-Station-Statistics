# Code Challenge Template

## Start
Before constructing the database, I wanted to become more familiar with the data. I copied a portion of the first file as a sample. Then I wrote a Python script to read and parse the information from a tab delimited format. The script was expanded to read a sample file in the data file path (wx_data). Then I read in all of the actual files and also grabbed the weather station name from the text file name.

## Database - using postgres and SQL
Then I constructed the database using postgres and SQL statements. I used postgres because it was fresh on my mind from a prior project. I also used SQL statements instead of an ORM because I am very familiar with SQL. In postgres I created a database called testdb. The first of two main tables created was called weather_info.

CREATE TABLE weather_info (
    weather_info_id SERIAL PRIMARY KEY,
    weather_station varchar(256) DEFAULT NULL,
    weather_date date DEFAULT NULL,
    max_temp int DEFAULT NULL,
    min_temp int DEFAULT NULL,
    precip int DEFAULT NULL
);

I first established the database connection between Python and postgres, using the standard port 5432. I did a pip install psycopg2 for Python. After the initial connection, I modified the script to hide the database information using a file called database.ini. I used two scripts, one called config.py to read the database.ini file and a second called connect.py.

Then I wrote a script to read in a single file with 10 sample records and write it to the table created in the db. Once I verified that the data was writing correctly, I dropped the table and recreated it. Then I modified the script - called read_files.py - to read all the files into the db in the table weather_info. I also added start and end times for the script, as well as a record count.

## Weather Stats
I created a second table in the db called weather_stats. Here is the SQL statement for this table:

CREATE TABLE weather_stats (
    weather_stats_id SERIAL PRIMARY KEY,
    weather_station_stats varchar(256) DEFAULT NULL,
    weather_year_stats int DEFAULT NULL,
    avg_max_temp float DEFAULT NULL,
    max_temp_count int DEFAULT NULL,
    avg_min_temp float DEFAULT NULL,
    min_temp_count int DEFAULT NULL,
    total_accum_precip float DEFAULT NULL,
    precip_count int DEFAULT NULL
);

I decided to include valid record counts for the max and min temperature, as well as a precipitation count, in case that this information might be requested in the future. I used a SQL select statement to order the information by station and date:

select * from weather_info order by weather_station, weather_date

I used the script calculate_stats.py, initially with a small data sample. The order allows for calculations to be in station order, with the years in order with the station. Once the small data samples were writing to the correct table and variables, I modified it to include information from multiple stations and years. 
     

