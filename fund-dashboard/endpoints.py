from quart import Quart, jsonify  # Import from Quart instead of Flask
from quart_cors import cors  # Quart-compatible CORS handling
import asyncio
import os
from dotenv import load_dotenv
from data_helpers import GetDataFromDatabase

load_dotenv()

app = Quart(__name__)  # Use Quart instead of Flask
app = cors(app)  # Enable CORS in a Quart-compatible way

@app.route("/api/get_daily_nav", methods=['GET'])
async def get_daily_nav():  # async works naturally in Quart
    # Use asyncio to run the I/O-bound task in a non-blocking way
    daily_nav = await asyncio.to_thread(GetDataFromDatabase.get_daily_nav)
    d3_data = [{"date": d.strftime("%Y-%m-%d"), "nav": float(nav)} for d, nav in daily_nav]
    return jsonify({
        "daily_nav": d3_data
    })

@app.route("/api/get_drawdown", methods=['GET'])
async def get_drawdowns():  # async works naturally in Quart
    # Use asyncio to run the I/O-bound task in a non-blocking way
    drawdown_array = await asyncio.to_thread(GetDataFromDatabase.get_drawdown_series)
    d4_data = [{"date": d.strftime("%Y-%m-%d"), "drawdown": float(drawdown)} for d, drawdown in drawdown_array]
    return jsonify({
        "drawdown_array": d4_data
    })

if __name__ == "__main__":
    # Quart is ASGI-compatible; use Hypercorn to run it
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5009"]
    config.debug = True

    # Run the app using Hypercorn's serve function
    asyncio.run(serve(app, config))
