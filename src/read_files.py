import os
import csv

def read_file_list(cur, conn):
   # The path for the location of the data directory
   data_path = "C:\\Users\\markl\\code-challenge-template\\wx_data"
   record_id = 0
   # Change directory to the data path
   os.chdir(data_path)
   # Check each file in the directory
   for file in os.listdir():
      if file.endswith('.txt'):
         f = open(file, "r")
         tsv_file = csv.reader(f, delimiter='\t')
         for line in tsv_file:
            (weather_date, max_temp, min_temp, precip) = line
            station = os.path.splitext(file)[0]
            cur.execute("INSERT INTO weather_info VALUES (%s, %s, %s, %s, %s, %s)", (record_id, station, weather_date, max_temp, min_temp, precip))
            conn.commit()   
            record_id = record_id + 1

   print("total records = ", record_id)



