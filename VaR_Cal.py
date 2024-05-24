'''
This file aims to provide three functions to calculate the VaR of the portfolio
'''
import numpy as np
import pandas as pd
import yfinance as yf

# Parametric Method
tickers = ['msft', 'aapl', 'meta']

df = yf.download(tickers, start='2020-01-01')
df = df['Adj Close']

def metrics(df):
    mu = df.mean()
    sigma = df.std()
    return [mu, sigma]
print(metrics(df)[1])



def VaR_par():
    ...