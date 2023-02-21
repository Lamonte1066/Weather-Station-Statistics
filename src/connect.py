import psycopg2
import time
from config import config
from read_files import read_file_list

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

        read_file_list(cur, conn)
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
