import pandas as pd
import plotly
import plotly.graph_objs as go

#считываем файл с данными
data = pd.read_csv("/home/user/K1-K6_big_1000.csv")


#Make Plotly figure


fig1 = go.Scatter3d(x=data['Criteria'],
                    y=data['City'],
                    z=data['Value'],
                    marker=dict(opacity=0.9,
                                reversescale=True,
                                colorscale='Blues',
                                size=5),
                    line=dict (width=0.02),
                    mode='markers')

#Make Plot.ly Layout
mylayout = go.Layout(scene=dict(xaxis=dict(title="Criteria"),
                                yaxis=dict(title="City"),
                                zaxis=dict(title="Value")),)

#Plot and save html
plotly.offline.plot({"data": [fig1],
                     "layout": mylayout},
                     auto_open=True,
                     filename=("_3DPlot.html"))
