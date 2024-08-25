from flask import Flask, render_template
import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

def fetch_data():
    response = requests.get('http://localhost:5000/api/get_daily_nav')
    data = response.json()
    return data['daily_nav']

def transform_data(daily_nav):
    dates = []
    navs = []
    
    for entry in daily_nav:
        date = pd.to_datetime(entry[0])
        nav = float(entry[1])
        dates.append(date)
        navs.append(nav)
    
    df = pd.DataFrame({
        'Date': dates,
        'NAV': navs
    })
    
    return df

@app.route('/')
def index():
    daily_nav = fetch_data()
    df = transform_data(daily_nav)

    min_nav = df['NAV'].min()
    max_nav = df['NAV'].max()
    pct_change = round(((max_nav - min_nav) / min_nav) * 100, 1)

    fig = px.line(df, x='Date', y='NAV', title="Daily NAV", template='plotly_dark')
    fig.update_layout(
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis=dict(showgrid=False, zeroline=False, title=None),
        yaxis=dict(showgrid=False, zeroline=False),
        width = 300,
        height = 300
    )
    fig.update_traces(mode='lines', line_shape='spline', line_color = "orange")

    graph_html = pio.to_html(fig, full_html=False)

    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
