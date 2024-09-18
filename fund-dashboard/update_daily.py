

from data_helpers import DrawDowns
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

SET_SAME_NAV = cur.execute("UPDATE fund_data SET percentage = 0 WHERE percentage IS NULL;")


def insert_same_zero_nav():
    correct_nav = []
    cur.execute("SELECT date, nav FROM fund_data ORDER BY date")
    rows = cur.fetchall()
    last = None
    for row in rows:
        row = list(row)
        if row[1] is None:
            row[1] = last
        last = row[1]

        correct_nav.append((row[0], row[1]))

    for date, nav in correct_nav:
        cur.execute("UPDATE fund_data SET nav = %s WHERE date = %s", (nav, date))

def insert_same_zero_aum():
    correct_aum = []
    cur.execute("SELECT date, aum FROM fund_data ORDER BY date")
    rows = cur.fetchall()
    last = None
    for row in rows:
        row = list(row)
        if row[1] is None:
            row[1] = last
        last = row[1]

        correct_aum.append((row[0], row[1]))

    for date, aum in correct_aum:
        cur.execute("UPDATE fund_data SET aum = %s WHERE date = %s", (aum, date))

def making_pct_more_precise():
    print("Func Started")
    cur.execute("SELECT date, nav FROM fund_data ORDER BY date")
    rows = cur.fetchall()

    nav_series = [row[1] for row in rows]  
    id_series = [row[0] for row in rows] 

    pct_series = [0]
    length = len(nav_series)

    for i in range(1, length):
        print("Nav Serires", i)
        pct = (nav_series[i] - nav_series[i-1]) / nav_series[i-1]  
        pct_series.append(pct)

    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='fund_data' AND column_name='precise_pct'")
    result = cur.fetchone()
    
    print(result)
    if not result: 
        print("Created")
        cur.execute("ALTER TABLE fund_data ADD COLUMN precise_pct NUMERIC(10, 6)") 
        print("Created")

    for i in range(0, length):  
        print("Updating Data ", i)
        cur.execute("UPDATE fund_data SET precise_pct = %s WHERE date = %s", (pct_series[i], id_series[i]))


#insert_same_zero_aum()
#insert_same_zero_nav()
making_pct_more_precise()

conn.commit()
conn.close()