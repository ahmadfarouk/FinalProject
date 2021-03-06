from flask import Flask, jsonify, render_template, request, redirect
import os
from fbprophet import Prophet
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import datetime
import datetime as dt

symbol = 'AMZN'

def save_dataset(symbol):
    api_key = 'P33J9T7IVI663Y0A'
    print (symbol)
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol, outputsize='full')
    filename = './templates/DataOutput/daily.csv'
    data.to_csv(filename)

def csv_to_dataset_fbprophet(csv_path):
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

def export_csv_to_html(csv_file):
    data = pd.read_csv(csv_file)
    data.to_html('./templates/DataOutput/AlphaVantage_daily_data.html')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/Stock_info')
def stock_info():
    return render_template("stock_info.html")

@app.route('/api/submit_form', methods=['POST'])
def submit_form():
        symbol = request.form['symbol']
        save_dataset(symbol)
        PredictStockFB()
        PredictStockLR()

        return redirect("/")

def PredictStockFB():
    data,data_openclose, data_volume, data_high, data_low = csv_to_dataset_fbprophet(f'./templates/DataOutput/daily.csv')
    
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

    model_openclose.plot(predictions_openclose)
    plt.ylabel("Open-Close Price ", rotation='vertical', weight='bold')
    plt.xlabel("Year",weight='bold')
    plt.savefig(f"static/images/Open_Close.png")
    plt.clf()
    plt.close()
    
    model_volume.plot(predictions_volume)
    plt.ylabel("Volume ", rotation='vertical', weight='bold')
    plt.xlabel("Year",weight='bold')
    plt.savefig(f"static/images/Volume.png")
    plt.clf()
    plt.close()

    model_high.plot(predictions_high)
    plt.ylabel("High Price ", rotation='vertical', weight='bold')
    plt.xlabel("Year",weight='bold')
    plt.savefig(f"static/images/HighPrice.png")
    plt.clf()
    plt.close()

    model_low.plot(predictions_low)
    plt.ylabel("Low Price ", rotation='vertical', weight='bold')
    plt.xlabel("Year",weight='bold')
    plt.savefig(f"static/images/LowPrice.png")
    plt.clf()
    plt.close()
    
    export_csv_to_html('./templates/DataOutput/daily.csv')

def PredictStockLR():
    stock = pd.read_csv('./templates/DataOutput/daily.csv')
    stock.rename(columns={'date': 'Date',
                        '1. open': 'Open',
                       '2. high': 'High',
                        '3. low': 'Low',
                        '4. close': 'Close',
                        '5. volume': 'Volume'}, inplace=True)
    print ('started LR')
    stock['Date']= pd.to_datetime(stock['Date'])
    start_date = min (stock['Date'])
    stock['NumberOfDays'] = (stock['Date'] - start_date).dt.days
    
    X = stock['NumberOfDays'].values.reshape (-1,1)
    y = stock['Close'].values.reshape (-1,1)
    
    print("Shape: ", X.shape, y.shape)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    lr=LinearRegression()
    lr.fit(X_train, y_train)
    close_predictions=lr.predict(X_test)
    Date_Test = []
    for i in range (len (X_test)):
        Date_Test.append(start_date + dt.timedelta(days=int(X_test[i][0])))
    print(lr.score(X_train, y_train))
    print(lr.score(X_test, y_test))

    last_date = max (stock['Date'])
    max_NumberOfDays = max (stock['NumberOfDays'])

    New_Xs = []
    for i in range (1, 90):
        New_Xs.append (max_NumberOfDays + i)
    NewXs = pd.DataFrame (New_Xs)
    X_future = NewXs.values.reshape (-1,1)
    future_predictions=lr.predict(X_future)
    for i in range (len (future_predictions)):
        Date_Test.append(start_date + dt.timedelta(days=int(X_future[i][0])))
    All_predictions = np.append (close_predictions, future_predictions)
    plt.scatter(Date_Test, All_predictions)
    plt.xlabel("Date",fontsize=20)
    plt.ylabel("Predicted Closing", fontsize=20)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.rcParams["figure.figsize"] = (70,40)
    plt.savefig("static/images/LR_ClosePrice.png")
    plt.clf()
    plt.close()
    print ('done LR')

####display All data
@app.route("/AV_data")
def AV_data():
    return render_template("DataOutput/AlphaVantage_daily_data.html")

if __name__ == "__main__":
    app.run(host='localhost', debug=True)