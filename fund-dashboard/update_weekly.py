
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def extract_nav_from_fund_data():
    cur.execute("""UPDATE weekly_data
    SET start_nav = subquery.nav
    FROM (
        SELECT wd.week_start, fd.nav
        FROM weekly_data wd
        JOIN fund_data fd
        ON wd.week_start = fd.date
    ) AS subquery
    WHERE weekly_data.week_start = subquery.week_start;
                """)
    
def extract_aum_from_fund_data():
    cur.execute(""" 
    UPDATE weekly_data
    SET aum = subquery.aum
    FROM (
        SELECT wd.week_start, fd.aum
        FROM weekly_data wd
        JOIN fund_data fd
        ON wd.week_start = fd.date
    ) AS subquery
    WHERE weekly_data.week_start = subquery.week_start; """)

def updating_percentage():
    cur.execute("SELECT week_start, start_nav FROM weekly_data ORDER BY week_start")
    rows = cur.fetchall()

    final_storage = []
    for date, start_nav in rows:
        final_storage.append([date, start_nav])
    
    pct = []
    for i in range(1, len(final_storage)):
        prev_nav = final_storage[i-1][1]
        curr_nav = final_storage[i][1]

        nav_pct = (curr_nav - prev_nav) / prev_nav
        pct.append((final_storage[i][0], nav_pct))

    print(pct)
    for date, pct_weekly in pct:
        cur.execute("UPDATE weekly_data SET percentage = %s WHERE week_start = %s", (pct_weekly, date))

if __name__ == "__main__":

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    conn.commit()
    cur.close()
    conn.close()
