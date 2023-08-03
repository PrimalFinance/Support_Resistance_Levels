# Number manipulation
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
# Stock data
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
# Date calculations
import datetime as dt
# Graph creation 
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# Trendline library
from TradeRanges.trend_lines import TrendLines


# API Keys
from API_Keys.api_keys import alpha_vantage_key







class TradeRanges:
    def __init__(self, ticker: str, months: int, data_source: str = "Yahoo") -> None:
        '''
        ticker: The stock code for the company.
        months: Window of time for our data. If months = 5, we will start 5 months before the current date.
        data_source: Data can be fetched from Yahoo Finance by passing "Yahoo" in the parameter, or
        Alpha Vantage, by passing "Alpha" in the parameter.
        '''
        self.ticker = ticker
        self.month_range = months
        self.data_source = data_source
        self.trend_start_offset = 0
        self.stock_data = pd.DataFrame()

        self.set_stock_data()

        self.trend_lines = TrendLines(self.ticker, self.stock_data)

        #self.trend_lines.get_trendlines()



    '''--------------------------------------'''
    def set_stock_data(self) -> None:


        if self.data_source == "Yahoo":
            # Get the start and end date for our window of time. 
            start_date, end_date = self.get_start_end_dates()
            # Convert datetime objects to strings.
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")
            # Download data from Yahoo Finance.
            self.stock_data = yf.download(self.ticker, start=start_date_str, end=end_date_str)
        elif self.data_source == "Alpha":
            ts = TimeSeries(key=alpha_vantage_key, output_format='pandas')
            interval="5min"
            # Retrieve intra-day stock data
            self.stock_data, meta_data = ts.get_intraday(symbol=self.ticker, interval=interval, outputsize='full')
            self.stock_data.columns = ["Open", "High", "Low", "Close", "Volume"]

            print(f"Data: {self.stock_data}")
    '''--------------------------------------'''
    def get_stock_data(self) -> pd.DataFrame:
        if self.stock_data.empty:
            self.set_stock_data(month_range=self.month_range)
        return self.stock_data
    '''--------------------------------------'''
    '''--------------------------------------'''
    def get_start_end_dates(self):
        end_date = dt.datetime.now().date()

        start_date = end_date - dt.timedelta(days=self.month_range * 30)

        return start_date, end_date    
    '''--------------------------------------'''
    def plot_graph(self, resistance: int, support: int) -> None:
        if self.stock_data.empty:
            self.set_stock_data()

        # Create figure
        plt.figure(figsize=(10,6))
        # Plot the data from the "Adjusted Close" column
        plt.plot(self.stock_data['Adj Close'])
        # Add title
        plt.title(f"{self.ticker} Trading Ranges")
        # Create x-axis label
        plt.xlabel("Date")
        # Create y-axis label
        plt.ylabel("Price (USD)")
        plt.grid(True)

        # Create rolling values in dataset
        rolling_min = self.stock_data["Adj Close"].rolling(window=self.month_range*30, min_periods=1).min()
        rolling_max = self.stock_data["Adj Close"].rolling(window=self.month_range*30, min_periods=1).max()

        # Create resistance line
        resistance = 2 * rolling_max - rolling_min
        plt.plot(self.stock_data.index, resistance, label="Resistance", linestyle="--", color="red")

        # Create support line
        support = 2 * rolling_min - rolling_max
        plt.plot(self.stock_data.index, support, label="Support", linestyle="--", color="blue")
        
        # Create resistance line.
        ''' resistance_line = np.polyfit(np.arange(len(self.stock_data["Adj Close"])), self.stock_data["Adj Close"], 1)
        resistance_line_values = np.polyval(resistance_line, np.arange(len(self.stock_data["Adj Close"])))
        plt.plot(self.stock_data.index, resistance_line_values, color="b", linestyle="--", label = "Resistance Trendline")
        # Create support line.
       
        support_line = np.polyfit(local_min_indexes, local_min_values, deg=2)
        support_line_values = np.polyval(support_line, np.arange(len(self.stock_data["Adj Close"])))
        plt.plot(self.stock_data.index, support_line_values, color="r", linestyle="--", label="Support Trendline")'''


        plt.legend() 
        plt.show()
    '''--------------------------------------'''
    def plot_graph_v2(self):

        # Get the indexes 
        indexes = self.trend_lines.indexes


        e = indexes[-1]
        if self.data_source == "Yahoo":
            s = indexes[0]
            stock_data = self.stock_data
        elif self.data_source == "Alpha":
            s = indexes[-200]
            stock_data = self.stock_data[s:e]
            self.trend_lines.set_stock_data(stock_data)
        



        fig = go.Figure(data=[go.Candlestick(x=indexes,
                                             open=stock_data["Open"],
                                             high=stock_data["High"],
                                             low=stock_data["Low"],
                                             close=stock_data["Close"])])
        

       
        

        

        support, resistance = self.trend_lines.get_trendlines(data=stock_data)

        support = self.delete_overlapping_trends(support)            
        resistance = self.delete_overlapping_trends(resistance)
        


        self.add_trendline(figure=fig,
                           data=support,
                           color="Green",
                           end=e)
        
        self.add_trendline(figure=fig,
                           data=resistance, 
                           color="Red",
                           end=e)

        
        fig.show()
    '''--------------------------------------'''
    def delete_overlapping_trends(self, plotlist, sensitivity: float = 0.005):
        '''
        plotlist: List of data containing Support or Resistance levels. 
        sensitivity: Determines the conditions for trends to be removed. The lower the value, the more sensitive. 
        '''

        print(plotlist)

        for i in range(1, len(plotlist)):
            if (i>=len(plotlist)):
                break
            if abs(plotlist[i][1]-plotlist[i-1][1]) <= sensitivity:
                plotlist.pop(i) 
            
        return plotlist

    '''--------------------------------------'''
    def add_trendline(self, figure,data, color: str, end: int):

        c=0
        while (1):
            if (c>len(data)-1):
                break
            figure.add_shape(type="line", x0=data[c][0] - self.trend_start_offset, y0=data[c][1],
                            x1=end,
                            y1=data[c][1], 
                            line=dict(color=color))
            c+= 1

    '''--------------------------------------'''
    '''--------------------------------------'''
    '''--------------------------------------'''

