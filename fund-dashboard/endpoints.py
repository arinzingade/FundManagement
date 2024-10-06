from quart import Quart, jsonify 
from quart_cors import cors  
import asyncio
import os
from dotenv import load_dotenv
from data_helpers import GetDataFromDatabase
from datetime import datetime

load_dotenv()

app = Quart(__name__)  
app = cors(app) 

@app.route("/api/get_daily_nav", methods=['GET'])
async def get_daily_nav(): 
    daily_nav = await asyncio.to_thread(GetDataFromDatabase.get_daily_nav)
    d3_data = [{"date": d.strftime("%Y-%m-%d"), "nav": float(nav)} for d, nav in daily_nav]
    return jsonify({
        "daily_nav": d3_data
    })

@app.route("/api/get_drawdown", methods=['GET'])
async def get_drawdowns():  
    drawdown_array = await asyncio.to_thread(GetDataFromDatabase.get_drawdown_series)
    d4_data = [{"date": d.strftime("%Y-%m-%d"), "drawdown": float(drawdown)} for d, drawdown in drawdown_array]
    return jsonify({
        "drawdown_array": d4_data
    })

@app.route("/api/get_ratios", methods = ['GET'])
async def get_ratios():

    start = datetime.now()

    alltime_ret = await asyncio.to_thread(GetDataFromDatabase.get_alltime_return) 
    win_rate_list = await asyncio.to_thread(GetDataFromDatabase.get_daily_win_pct) 
    alpha = await asyncio.to_thread(GetDataFromDatabase.get_alpha) 

    end = datetime.now()
    time_taken = end - start

    return jsonify({
        "all_time_return": int(alltime_ret[0]),
        "win_rate": win_rate_list[0],
        "loss_rate": win_rate_list[1],
        "journey": win_rate_list[2],
        "current_nav": float(alltime_ret[1]),
        "alpha": alpha[0],
        "annualised_vol": alpha[1],
        "cagr": alpha[2],
        "sharpe": alpha[3],
        "beta": alpha[4],
        "time_taken": str(time_taken)
    })

@app.route("/api/put_pnl", methods = ['POST'])
async def put_pnl():
    pass


if __name__ == "__main__":
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5009"]
    config.debug = True

    # Run the app using Hypercorn's serve function
    asyncio.run(serve(app, config))
