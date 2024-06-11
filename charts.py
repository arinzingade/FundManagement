
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
        
        gdfc = GenerateData_ForCharts()
        fund_data = gdfc.GenerateNAVChart()
        nav = fund_data[0]
        dates = fund_data[1]
        dates = pd.to_datetime(dates)
        
        df = pd.DataFrame({
            'x': dates,
            'y': nav
        })

        df.sort_values('x', inplace=True)
        
        chart = px.line(df, x='x', y='y')
        chart.update_traces(line_color = 'yellow')

        chart.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  
            paper_bgcolor='rgba(0,0,0,0)',  
            xaxis=dict(
                linecolor='rgba(222,222,222,222)',  
                gridcolor='rgba(0,0,0,0)',  
                tickfont=dict(
                    color='rgba(222,222,222,222)'  
                ),
                titlefont=dict(
                    color='rgba(222,222,222,222)' 
                ),
            ),
            yaxis=dict(
                linecolor='rgba(222,222,222,222)', 
                gridcolor='rgba(0,0,0,0)',
                 tickfont=dict(
                    color='rgba(222,222,222,222)' 
                ),
                titlefont=dict(
                    color='rgba(222,222,222,222)'  
                )
            )
        )
        print(nav)
        return chart

       