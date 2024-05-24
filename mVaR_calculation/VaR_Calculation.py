import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm
from VaR_function import *

# Download Data
xls = pd.ExcelFile('./data/GEPC.xlsx')
df_price = pd.read_excel(xls, 'Global Equity Price Change', index_col= 'Date')
df_weight = pd.read_excel(xls, 'Weight', index_col = 'Company')


# Calculate necessary metrics to calculate VaR
df_pctc = df_price / 100
mu, sigma, cov, cor = metrics(df_pctc)
weight = df_weight['Quantity'] / sum(df_weight['Quantity'])
price = df_weight['Price']
df_weight['mkt_value'] = df_weight['Price'] * df_weight['Quantity']
market_value = sum(df_weight['mkt_value'])
print(market_value)

VaRParametrics = var_pmtrc(market_value, weight, mu, sigma, cov)
VaRHistorical = var_hist(market_value, df_pctc, weight)
VaRMC = VaR_mc(market_value, mu, sigma, cov, weight)

df_VaR = pd.DataFrame({
    'Method': ['Parametric', 'Historical', 'Monte Carlo'],
    'VaR': [VaRParametrics, VaRHistorical, VaRMC]
})

# We use the parametric method to calculate the marginal VaR for each ticker

mVaR = []
sector = []
tickers = df_weight.index

for ticker in tickers:
    df_drop = df_pctc.drop(ticker, axis=1)
    mu_drop, sigma_drop, cov_drop, cor_drop = metrics(df_drop)
    df_weight_drop = df_weight.drop(ticker, axis=0)
    
    market_value_drop = df_weight_drop['mkt_value'].sum()
    weight_drop = df_weight_drop['Quantity'] / df_weight_drop['Quantity'].sum()
    VaR2 = var_pmtrc(market_value_drop, weight_drop, mu_drop, sigma_drop, cov_drop)
    
    ticker_market_value = df_weight.loc[ticker]['Price'] * df_weight.loc[ticker]['Quantity']
    mVaR.append((VaRParametrics - VaR2) / ticker_market_value)
    t = yf.Ticker(ticker)
    sector.append(t.info['sector'])

df_mVaR = pd.DataFrame({'Ticker':df_weight.index, 'mVaR':mVaR, 'sector':sector})


# We use the parametric method to calculate the marginal VaR for each sector
df_weight['sector'] = sector
mVaR_sector = []
df_sector_mkt_value = df_weight.groupby(sector).sum()['mkt_value']
sectors = df_sector_mkt_value.index

for s in sectors:
    df_drop = df_weight[df_weight['sector'] != s]
    df_s = df_weight[df_weight['sector'] == s]
    market_value_drop = df_drop['mkt_value'].sum()
    market_value_s = df_s['mkt_value'].sum()
    weight_drop = df_drop['Quantity'] / df_drop['Quantity'].sum()

    ticker_drop = df_drop.index
    mu_drop, sigma_drop, cov_drop, cor_drop = metrics(df_pctc[ticker_drop])
    VaR2 = var_pmtrc(market_value_drop, weight_drop, mu_drop, sigma_drop, cov_drop)

    mVaR_sector.append((VaRParametrics - VaR2) / market_value_s)

df_mVaR_sector = pd.DataFrame({
    'Sector': sectors,
    'mVaR': mVaR_sector
})
    


print(df_mVaR_sector)
print(df_mVaR)
print(df_VaR)

fileName_mVaR = 'mVaR.xlsx'
fileName_mVaR_sector = 'mVaR_sector.xlsx'
fileName_VaR = 'VaR.xlsx'

df_VaR.to_excel(fileName_VaR)
df_mVaR.to_excel(fileName_mVaR)
df_mVaR_sector.to_excel(fileName_mVaR_sector)

