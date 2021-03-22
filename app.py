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

