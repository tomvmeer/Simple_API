from flask import Flask
import flask
import plotly.graph_objects as go
import plotly
import numpy as np
from sklearn.datasets import make_moons
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import json
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)


@app.route('/')
def figure_builder():
    # load dataset
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv")

    # create figure
    fig = go.Figure()

    # Add surface trace
    fig.add_trace(go.Surface(z=df.values.tolist(), colorscale="Viridis"))
    # Update plot sizing
    fig.update_layout(
        height=700,
        autosize=False,
        margin=dict(t=100, b=0, l=0, r=0),
    )

    # Update 3D scene options
    fig.update_scenes(
        aspectratio=dict(x=1, y=1, z=0.7),
        aspectmode="manual"
    )

    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=["type", "surface"],
                        label="3D Surface",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "heatmap"],
                        label="Heatmap",
                        method="restyle"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.11,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    # Add annotation
    fig.update_layout(
        annotations=[
            dict(text="Trace type:", showarrow=False,
                 x=0, y=1.08, yref="paper", align="left")
        ]
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == '__main__':
    app.run()
