import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)
    
    ''' Inserting individual record to songs table
    # insert song record
    # song_data = df.loc[:,['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    # cur.execute(song_table_insert, song_data)
    '''
    
    ## Append the record to a file 'songs_data.csv'
    with open('songs_data.csv', 'a') as fx:
        for index, row in df.iterrows():
            fx.write(row['song_id']+'|'+row['title']+'|'+ row['artist_id']+'|'+ str(row['year']) +'|'+ str(row['duration']) +'\n')
        
    ''' Inserting individual record artists table
    # insert artist record
    # artist_data = df.loc[:,['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    # cur.execute(artist_table_insert, artist_data)
    '''
    
    ## Append the record to a file 'artists_data.csv'
    with open('artists_data.csv', 'a') as fx:
        for index, row in df.iterrows():
            fx.write(row['artist_id']+'|'+row['artist_name']+'|'+ row['artist_location']+'|'+str(row['artist_latitude'])+'|'+str(row['artist_longitude'])+'\n')
        
def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    df['dts'] = pd.to_datetime(df['ts'])
    
    # insert time data records
    time_data = ([row['ts'], row['dts'].hour, row['dts'].day, row['dts'].weekofyear,\
                  row['dts'].month, row['dts'].year, row['dts'].weekday()] for index, row in df.iterrows())

    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    
    time_df = pd.DataFrame(time_data, columns= column_labels)
    
    ## Append each row to a file 'time_data.csv'
    with open('time_data.csv', 'a') as fx:
        for i, row in time_df.iterrows():
            # cur.execute(time_table_insert, list(row))
            fx.write(str(row['start_time'])+'|'+str(row['hour'])+'|'+\
                    str(row['day'])+'|'+str(row['week'])+'|'+str(row['month'])+'|'+\
                    str(row['year'])+'|'+str(row['weekday'])+'\n')

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]
    
    ## Append each row to a file 'users_data.csv'
    with open('users_data.csv', 'a') as fx:
        # insert user records
        for i, row in user_df.iterrows():
            # cur.execute(user_table_insert, row)
            fx.write(str(row['userId'])+'|'+row['firstName']+'|'+\
              row['lastName']+'|'+row['gender']+'|'+row['level']+'\n')
    
    ## Append each row to a file 'songplays_data.csv'
    with open('songplays_data.csv', 'a') as fx:
        # insert songplay records
        for index, row in df.iterrows():

            # get songid and artistid from song and artist tables
            cur.execute(song_select, (row.song, row.artist, row.length))
            results = cur.fetchone()

            if results:
                songid, artistid = results
            else:
                songid, artistid = '',''#None, None
            
            '''
            # insert songplay record
            # songplay_data = (str(row['ts']), int(row['userId']), row['level'], songid,\
            #                 artistid, row['sessionId'], row['location'], \
            # print(row)
            # print(str(row['ts'])+'|'+str(row['userId'])+'|'+\
                     # row['level']+'|'+str(songid)+'|'+\
                     # artistid+'|'+str(row['sessionId'])+'|'+row['location']+'|'+ \
                     # str(row['userAgent'])+'\n')
            # cur.execute(songplay_table_insert, songplay_data)
            '''         
                    
            fx.write(str(row['ts'])+'|'+str(row['userId'])+'|'+\
                     row['level']+'|'+str(songid)+'|'+\
                     artistid+'|'+str(row['sessionId'])+'|'+row['location']+'|'+ \
                     row['userAgent'].strip('"')+'\n')

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        # conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    dataFiles = ['songs_data.csv', 'artists_data.csv',\
                'users_data.csv', 'time_data.csv', \
                'songplays_data.csv']
    
    ## create the data files
    for file in dataFiles:
        with open(file, 'w') as fp: 
            pass

    
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    
    ## Remove duplicats in first three files 
    ## by replacing the old one with the last one
    for file in dataFiles[:3]:
        temp_df = pd.read_csv(file, sep='|', header=None)
        # print(temp_df.head())
        temp_df.drop_duplicates(subset=[0], keep='last', inplace=True)
        temp_df.to_csv(file, sep='|', header=False, index=False)
    
    ## Add the index columnt o the songplays_data
    temp_df = pd.read_csv('songplays_data.csv', sep='|', header=None)
    temp_df.to_csv('songplays_data.csv', sep='|', header=False, index=True)
    
    ## bulk insert using copy_from
    for file in dataFiles:
        table = file.split('_')[0]
        f = open(file, 'r')
        print(file)
        cur.copy_from(f, table, sep='|', null='')
        f.close()
        conn.commit()

    conn.close()


if __name__ == "__main__":
    main()