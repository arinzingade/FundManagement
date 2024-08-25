from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv
from data_helpers import GetDataFromDatabase

load_dotenv()

app = Flask(__name__)

@app.route("/api/get_daily_nav", methods=['GET'])
def get_daily_nav():
    daily_nav = GetDataFromDatabase.get_daily_nav()
    return jsonify({
        "daily_nav": daily_nav
    })

if __name__ == "__main__":
    app.run(debug=True)
