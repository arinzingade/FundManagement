
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from flask import Flask, render_template
import pandas as pd

from functions import GenerateData_ForCharts
from dockerpy import clientLinkClass


ck = clientLinkClass()
client = ck.clientLink(True)
db = client['mydatabase']
fund_info = db['fund']

y = []
for i in range(0,298):
    y.append(i)


class LineCharts:
    
    def NavChart():
        

        # Retrieve data from MongoDB collection
        data = list(fund_info.find({}))

        # Initialize lists to store nav and date
        nav_price_list = []
        date_list = []

        # Process each document in the data list
        for doc in data:
            nav_price_list.append(doc['nav'])
            date_list.append(doc['date'])

        # Convert date_list to datetime
        date_list = pd.to_datetime(date_list)

        # Create a DataFrame from the lists
        df = pd.DataFrame({'Date': date_list, 'NAV': nav_price_list})

        # Plot the data using Plotly Express with custom styling
        fig = px.line(df, x='Date', y='NAV', title='NAV Price Over Time', 
                    line_shape='spline')  # Make the line curvy

        # Update line color to yellow and background color
        fig.update_traces(line=dict(color='yellow'))
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
            title_font=dict(size=24, color='white'),
            xaxis_title_font=dict(size=18, color='white'),
            yaxis_title_font=dict(size=18, color='white'),
            font=dict(size=12, color='white'),
            xaxis=dict(
                gridcolor='gray', 
                zerolinecolor='gray',  
            ),
            yaxis=dict(
                gridcolor='gray', 
                zerolinecolor='gray',
            )
        )

        fig.show()


       