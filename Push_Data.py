import csv
import psycopg2

host = ""
port = "5432"
user = ""
password = ""
region = "us-east-1"
dbname = "cognitive_lab_database"

conn = None
cur = None

def push_redditdata(conn, cur):
    with open('reddit_data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.
        for row in reader:
            cur.execute(
                "INSERT INTO reddit_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                row
            )
        conn.commit()

def push_redditdata_comments(conn, cur):
    with open('reddit_data_comments.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.
        for row in reader:
            cur.execute(
                "INSERT INTO reddit_data_comments VALUES (%s, %s, %s, %s, %s, %s, %s)",
                row
            )
        conn.commit()

try:
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password, port=port)
    cur = conn.cursor()
    push_redditdata(conn, cur)
    push_redditdata_comments(conn, cur)
except Exception as error:
    print(error)
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()

print('Process Complete!')