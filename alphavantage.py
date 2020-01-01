from alpha_vantage.timeseries import TimeSeries
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import numpy as np

class Stonks:

    def __init__(self, ticker, timeframe, mode):
        self.ts = TimeSeries(key='RI148SC1TRRU91UD', output_format='pandas', indexing_type='integer')
        self.ticker = ticker 
        self.timeframe = timeframe
        self.mode = mode
        self.data, self.meta_data = self.slice_ticker_data()
        self.data['index'] = pd.to_datetime(self.data['index'])

    def fix_date(self):
        self.data['index'] = pd.to_datetime(self.data['index'])  

    def slice_ticker_data(self):
    #     response = request.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker +"&outputsize=full&apikey=RI148SC1TRRU91UD")
        data, meta_data = self.ts.get_daily(symbol=self.ticker ,outputsize='full')
        if self.mode == 0:
            self.timeframe *= 31
        else:
            self.timeframe*=7
        data = data[::-1]
        data = data[len(data)-1:len(data)-1-self.timeframe:-1]
        # data = data.drop('index', axis=1)
        return data, meta_data

    def plot_candlesticks(self):
        fig = go.Figure(data=[go.Candlestick(x=self.data['index'],
                open=self.data['1. open'],
                high=self.data['2. high'],
                low=self.data['3. low'],
                close=self.data['4. close'])])
        fig.update_layout(
            xaxis=go.layout.XAxis(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        fig.show()

    def plot_high_low(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(x = self.data['index'], y = self.data['3. low'], name = 'low'),
            secondary_y = False
        )

        fig.add_trace(go.Scatter(x = self.data['index'], y = self.data['2. high'], name = 'high'),
            secondary_y = False
        )

        fig.update_layout(
            xaxis=go.layout.XAxis(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        fig.show()

    def plot_predict(self, actual, prediction):
        x_vals = np.arange(60)
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(x = x_vals, y = actual, name = 'actual price'),
            secondary_y = False
        )

        fig.add_trace(go.Scatter(x = x_vals, y = prediction, name = 'predicted price'),
            secondary_y = False
        )

        fig.update_layout(
            xaxis=go.layout.XAxis(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        fig.show()


