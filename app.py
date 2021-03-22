from flask import Flask, jsonify, render_template
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

def csv_to_dataset_volume(csv_path):
    data = pd.read_csv(csv_path)

    return data

save_dataset('AC')

data,data_openclose, data_volume, data_high, data_low = csv_to_dataset_openclose('./DataOutput/AC_daily.csv')

print (data_openclose.head ())
print (data_volume.head ())
print (data_high.head ())
print (data_low.head ())

model_openclose = Prophet(daily_seasonality=True)
model_volume = Prophet(daily_seasonality=True)
model_high = Prophet(daily_seasonality=True)
model_low = Prophet(daily_seasonality=True)

model_openclose.fit(data_openclose)
model_volume.fit(data_volume)
model_high.fit(data_high)
model_low.fit(data_low)

future_openclose_df = model_openclose.make_future_dataframe(periods=90)
future_volume_df = model_volume.make_future_dataframe(periods=90)
future_high_df = model_high.make_future_dataframe(periods=90)
future_low_df = model_low.make_future_dataframe(periods=90)

predictions_openclose = model_openclose.predict(future_openclose_df)
predictions_volume = model_volume.predict(future_volume_df)
predictions_high = model_high.predict(future_high_df)
predictions_low = model_low.predict(future_low_df)

ax =model_openclose.plot(predictions_openclose)
plt.ylabel("Open-Close Price ", rotation='vertical', weight='bold')
plt.xlabel("Year",weight='bold')
plt.savefig("./DataOutput/AC_Open_Close.png")

model_volume.plot(predictions_volume)
plt.ylabel("Volume ", rotation='vertical', weight='bold')
plt.xlabel("Year",weight='bold')
plt.savefig("./DataOutput/AC_Volume.png")

model_high.plot(predictions_high)
plt.ylabel("High Price ", rotation='vertical', weight='bold')
plt.xlabel("Year",weight='bold')
plt.savefig("./DataOutput/AC_HighPrice.png")

model_low.plot(predictions_low)
plt.ylabel("Low Price ", rotation='vertical', weight='bold')
plt.xlabel("Year",weight='bold')
plt.savefig("./DataOutput/AC_LowPrice.png")