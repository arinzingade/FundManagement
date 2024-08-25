import psycopg2
import numpy as np
from decimal import Decimal
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(url)
cur = conn.cursor()

class DrawDowns:

    def __init__(self):
        self.conn = psycopg2.connect(url)
        self.cur = self.conn.cursor()
        self.nav_values = self.get_data()
        self.drawdown_array = self.drawdowns()

    def get_data(self):
        try:
            self.cur.execute("SELECT date, nav FROM fund_data ORDER BY date")
            rows = self.cur.fetchall()
            values = [(row[0], row[1] if row[1] is not None else None) for row in rows]
            return values
        except Exception as e:
            print(f"An error occurred: {e}")

    def drawdowns(self):
        peak = None
        dd_array = []
        for id, nav in self.nav_values:
            if nav is None:
                dd_array.append((id, None))
                continue
            
            if peak is None:
                peak = nav
            else:
                peak = max(nav, peak)
            
            dd = min(((nav - peak) / peak), Decimal(0))
            dd_array.append((id, dd))
        
        return dd_array

    def update_data(self):
        try:
            for id, dd in self.drawdown_array:
                if dd is None:
                    self.cur.execute("UPDATE fund_data SET drawdowns = NULL WHERE id = %s", (id,))
                else:
                    self.cur.execute("UPDATE fund_data SET drawdowns = %s WHERE id = %s", (dd, id))
            
            self.cur.execute("UPDATE fund_data SET drawdowns = 0 WHERE drawdowns IS NULL")

            self.conn.commit()
            print("Drawdown values updated successfully.")
        
        except Exception as e:
            print(f"An error occurred while updating data: {e}")
        
        finally:
            self.cur.close()
            self.conn.close()

class GetDataFromDatabase():

    def __init__():
        pass

    def get_daily_nav():
        cur.execute("SELECT date, nav FROM fund_data ORDER BY date")
        rows = cur.fetchall()

        daily_nav = []
        for row in rows:
            daily_nav.append((row[0], row[1]))

        return daily_nav

    def get_weekly_nav():
        pass

    def get_monthly_nav():
        pass

    def get_quarter_nav():
        pass

    def get_drawdown_series():
        pass

    def get_ytd_returns():
        pass

    def get_daily_win_pct():
        pass

    def get_daily_loss_pct():
        pass

    def total_jouney():
        pass

    def current_nav():
        pass


class GetRatios():

    def __init__():
        pass


if __name__ == "__main__":
    GetDataFromDatabase.get_daily_nav()