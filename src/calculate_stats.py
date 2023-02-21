import psycopg2
import time
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    # Start time
    start_time = time.time()
    print("start time ", time.ctime(start_time))
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        query = "select * from weather_info order by weather_station, weather_date"
        cur.execute(query)
        for line in cur:
            records = cur.fetchall();
            print(len(records))
            #s = []
            #y = []
            previous_station = ""
            previous_year = ""

            total_max_temp = 0
            total_max_temp_count = 0
            total_min_temp = 0
            total_min_temp_count = 0
            total_precip = 0
            total_precip_count = 0
            id_count = 0
            for record in records:
                station = record[1]
                date = record[2]
                max_temp = record[3]
                min_temp = record[4]
                precip = record[5]
                if max_temp == -9999:
                    pass
                else:
                    total_max_temp += max_temp
                    total_max_temp_count += 1

                if min_temp == -9999:
                    pass
                else:
                    total_min_temp += min_temp
                    total_min_temp_count += 1

                if precip == -9999:
                    pass
                else:
                    total_precip += precip
                    total_precip_count += 1

                year = date.year

                if station != previous_station:
                    #s.append(station)
                    previous_station = station
                    total_max_temp = 0
                    total_max_temp_count = 0
                    total_min_temp = 0
                    total_min_temp_count = 0
                    total_precip = 0
                    total_precip_count = 0

                if year != previous_year:
                    previous_year = year
                    #y.append([station, year, total_max_temp, total_max_temp_count, total_min_temp, total_min_temp_count, total_precip, total_precip_count])
                    # Total accumulated maximum temperature divided by total max temp count
                    if total_max_temp_count > 0:
                        avg_max_temp = total_max_temp / total_max_temp_count
                        avg_max_temp = avg_max_temp / 10
                    else:
                        avg_max_temp = "0"

                    # Total accumulated minimum temperature divided by total min temp count
                    if total_min_temp_count > 0:
                        avg_min_temp = total_min_temp / total_min_temp_count
                        avg_min_temp = avg_min_temp / 10
                    else:
                        avg_min_temp = "0"

                    insert_query = """ insert into weather_stats (weather_stats_id, weather_station_stats, weather_year_stats,
                                        avg_max_temp, max_temp_count, avg_min_temp, min_temp_count, total_accum_precip, precip_count)
                                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    insert_record = (id_count, station, year, avg_max_temp, total_max_temp_count, avg_min_temp, total_min_temp_count, total_precip, total_precip_count)
                    cur.execute(insert_query, insert_record)
                    conn.commit()
                    count = cur.rowcount
                    id_count += 1
                    print(count, "Record inserted successfully into weather_stats table")

                    total_max_temp = 0
                    total_max_temp_count = 0
                    total_min_temp = 0
                    total_min_temp_count = 0
                    total_precip = 0
                    total_precip_count = 0

	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            end_time = time.time()
            print("--- %s seconds ---" % (end_time - start_time))
            print("end time ", time.ctime(end_time))


if __name__ == '__main__':
    connect()
