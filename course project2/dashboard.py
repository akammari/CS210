import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pymongo import MongoClient
import plotly.express as px
import pandas as pd
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

app = dash.Dash(__name__)

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

app.layout = html.Div([
    html.H1("Real-Time Twitter Sentiment Analysis"),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),
    dcc.Graph(id='live-graph')
])

@app.callback(Output('live-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    tweets = collection.find().sort('_id', -1).limit(100)
    df = pd.DataFrame(list(tweets))
    fig = px.pie(df, names='sentiment', title='Sentiment Analysis of Tweets')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
