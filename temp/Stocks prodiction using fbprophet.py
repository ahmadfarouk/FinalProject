from fbprophet import Prophet
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries

def save_dataset(symbol):
    api_key = 'P33J9T7IVI663Y0A'

    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol, outputsize='full')

    data.to_csv(f'./{symbol}_daily.csv')
    print (f'./{symbol}_daily.csv')

def csv_to_dataset(csv_path):
    data = pd.read_csv(csv_path)
    data.drop(columns=['1. open','2. high','3. low','5. volume'], axis=1, inplace=True)
    data.rename(columns={"date": "ds", "4. close": "y"}, inplace = True)
    return data

save_dataset('MSFT')

data = csv_to_dataset ('/content/drive/MyDrive/MachineLearning/MSFT_daily.csv')
data.head ()

model = Prophet(daily_seasonality=True)
model.fit(data)
data.tail()

future_df = model.make_future_dataframe(periods=365)
future_df

predictions = model.predict(future_df)
predictions

model.plot(predictions)
model.plot_components(predictions)

