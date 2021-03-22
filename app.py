from flask import Flask, jsonify, render_template
import pandas as pd
import datetime as dt

from fbprophet import Prophet
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries

def save_dataset(symbol):
    api_key = 'P33J9T7IVI663Y0A'

    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol, outputsize='full')

    data.to_csv(f'./DataOutput/{symbol}_daily.csv')
    print (data.head ())
    print (f'./DataOutput/{symbol}_daily.csv')

def csv_to_dataset_openclose(csv_path):
    data = pd.read_csv(csv_path)
    dateList = []
    yList = []
    row_count = len(data['1. open'])

    for i in range (row_count):
      dateList.append (str(data.date[i]) + ' 09:30:00')
      dateList.append (str(data.date[i]) + ' 16:00:00')
      yList.append (data['1. open'][i])
      yList.append (data['4. close'][i])

      data_openclose = pd.DataFrame ({'ds':dateList,'y':yList})
    
    data_volume = data.drop (["1. open",  "2. high",   "3. low",  "4. close"], axis=1)
    data_volume.rename (columns = {"date": "ds", "5. volume": "y"}, inplace = True)

    data_high = data.drop (["1. open",  "5. volume",   "3. low",  "4. close"], axis=1)
    data_high.rename (columns = {"date": "ds", "2. high": "y"}, inplace = True)    
    
    data_low = data.drop (["1. open",  "5. volume",   "2. high",  "4. close"], axis=1)
    data_low.rename (columns = {"date": "ds", "3. low": "y"}, inplace = True)    
    
    return data,data_openclose, data_volume, data_high, data_low

