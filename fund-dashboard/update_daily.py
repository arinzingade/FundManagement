

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


insert_same_zero_aum()

##dd = DrawDowns()
##dd.update_data()

conn.commit()
conn.close()