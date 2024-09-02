from flask import Flask, render_template
from flask_cors import CORS
import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5010)
