
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from flask import Flask, render_template
import pandas as pd

class LineCharts:
    
    def NavChart():
        
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [100, 250, 350, 1000, 1560]
        })
     
        chart = px.line(df, x='x', y='y', line_shape='spline')
        chart.update_traces(line_color = 'yellow')

        specific_points = [(2, 250), (4, 1000)]  # Example specific points
        for point in specific_points:
            x_point, y_point = point
            chart.add_trace(px.scatter(x=[x_point], y=[y_point]).data[0])
        
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
        return chart

fig = LineCharts.NavChart()
pio.write_html(fig, 'charts.html')
       