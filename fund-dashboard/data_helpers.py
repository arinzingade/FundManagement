import psycopg2
import numpy as np
from decimal import Decimal
import os
from dotenv import load_dotenv
from datetime import datetime
import yfinance as yf
import pandas as pd

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
        cur.execute("SELECT date, drawdowns FROM fund_data ORDER BY date")
        rows = cur.fetchall()

        drawdowns = []
        for row in rows:
            drawdowns.append((row[0], row[1]))

        return drawdowns

    def get_ytd_returns():
        pass

    def get_alltime_return():
        cur.execute("SELECT date, nav FROM fund_data ORDER BY date")
        rows = cur.fetchall()

        length = len(rows)
        last_nav = rows[length - 1][1]
        first_nav = 7

        alltime_ret = (last_nav - first_nav) / first_nav
        return [alltime_ret*100, last_nav]

    def get_daily_win_pct():
        cur.execute("SELECT date, precise_pct FROM fund_data ORDER BY date")
        rows = cur.fetchall()

        length = len(rows)
        num_pos = 0
        zeros = 0
        for row in rows:
            if (row[1] > 0):
                num_pos += 1
            if (row[1] == 0):
                zeros += 1

        real_days = length - zeros
        num_negs = real_days - num_pos
        return [num_pos / real_days, num_negs / real_days, real_days]
    
    def get_alpha():
        nifty_series = yf.download("^NSEI", start = "2023-03-01", end = "2024-08-10")['Adj Close']
        full_date_range = pd.date_range(start=nifty_series.index.min(), end=nifty_series.index.max(), freq='D') 
        series_reindexed = nifty_series.reindex(full_date_range)
        series_filled = series_reindexed.bfill()

        nifty_pct = []
        for i in range(365, len(series_filled)):
            pct = (series_filled.iloc[i] - series_filled.iloc[i-365]) / series_filled.iloc[i-365]
            nifty_pct.append(float(pct))

        cur.execute("SELECT date, nav FROM fund_data ORDER BY date")
        rows = cur.fetchall()

        nav_list = []
        for row in rows:
            nav_list.append(row[1])
        
        nav_pct = []
        for i in range(365, len(nav_list)):
            pct = (nav_list[i] - nav_list[i-365]) / nav_list[i-365]
            nav_pct.append(float(pct))
        
        alpha = []
        for i in range(len(nav_pct)):
            alpha.append(nav_pct[i] - nifty_pct[i])

        last = len(alpha) - 1

        risk_free = 0.07
        daily_nav_pct =  HelperFunctions.daily_returns(nav_list)
        daily_nifty_pct = HelperFunctions.daily_returns(series_filled)
        annualised_vol = HelperFunctions.vol_calculation(daily_nav_pct)
        annualised_return = HelperFunctions.annualised_returns(daily_nav_pct)
        cagr = HelperFunctions.cagr(nav_list)
        sharpe = (cagr - risk_free)/annualised_vol
        beta = HelperFunctions.linalg(daily_nav_pct, daily_nifty_pct)

        return (alpha[last], annualised_vol, cagr, sharpe, beta)

class HelperFunctions():

    def __init__():
        pass

    def vol_calculation(arr):
        daily_vol = np.std(arr)
        annualised_vol = float(daily_vol) * np.sqrt(252)

        return annualised_vol

    def daily_returns(arr):

        arr = np.array(arr)
        res = [0]
        length = len(arr)
        for i in range(1, length):
            pct = (arr[i] - arr[i-1])/arr[i-1]
            res.append(pct)
        return res
    
    def annualised_returns(daily_returns):
        daily_returns = np.array(daily_returns, dtype=float)
        cum_returns = np.prod(1 + daily_returns) - 1
        annualised_return = (1 + float(cum_returns)) ** (252 / len(daily_returns)) - 1

        return annualised_return

    def cagr(nav_list):
        first_value = float(7)
        last_value = float(nav_list[-1])
        print(last_value)

        start_date = datetime.strptime("2023-03-01", "%Y-%m-%d")
        end_date = datetime.now()

        days = (end_date - start_date).days

        print("Days: ", days)
        years = float(days / 365)

        print("Years: ", years)
        cagr_value = ((last_value / first_value) ** (1 / years)) - 1

        return cagr_value

    def correlation(x, y):
        x = np.array(x, dtype = float)
        y = np.array(y, dtype = float)

        mean_x = float(np.mean(x))
        mean_y = float(np.mean(y))
        p = (x - mean_x)
        q = (y - mean_y)

        return np.sum(p*q)/np.sqrt(np.sum(p**2)*np.sum(q**2))
    
    def linalg(x, y):
        
        r = -HelperFunctions.correlation(x, y)
        sx = float(np.std(x))
        sy = float(np.std(y))
        b = r*sy/sx
        
        return b

if __name__ == "__main__":
    GetDataFromDatabase.get_alpha()