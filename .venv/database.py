import sys
import datetime
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='livestream',
                            user='os.environ['DB_USERNAME']',#,
                            password='os.environ['DB_PASSWORD']')#)
    return conn

def thread_db(frame):
    conn = get_db_connection()
    cur = conn.cursor()
    id = datetime.datetime.now()
    cur.execute('INSERT INTO videoframe (id, frame, waktu)'
                'VALUES (%s, %s, %s)',
		    	(id, frame,id.time()))
    conn.commit()
    cur.close()
    conn.close()
    
    
if __name__ == '__main__':
    print("starting...")
    # main(sys.argv[1])
