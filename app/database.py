import psycopg2
import time
from psycopg2.extras import RealDictCursor

import sys, os
sys.path.append(os.path.abspath('../'))
import secret

while True:
    try:
        conn = psycopg2.connect(host=secret.host, database=secret.database, user=secret.user, password=secret.password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connectiong to database failed!")
        print("Error:", error)
        time.sleep(2)