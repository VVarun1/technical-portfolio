import psycopg2
# Implementation of SELECT ... FOR UPDATE SKIP LOCKED
def claim_job():
    conn = psycopg2.connect("dbname=jobs")
    cur = conn.cursor()
    cur.execute("SELECT id FROM jobs WHERE status='pending' FOR UPDATE SKIP LOCKED LIMIT 1")
    return cur.fetchone()
