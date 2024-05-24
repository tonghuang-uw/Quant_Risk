'''
This file aims to provide three functions to calculate the VaR of the portfolio
'''
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm

# Parametric Method

def metrics(pct_change):
    mu = pct_change.mean()
    sigma = pct_change.std()
    cov_mat = pct_change.cov()
    cor_mat = pct_change.corr()
    return [mu, sigma, cov_mat, cor_mat]


def var_pmtrc(market_value, weight, mu, sigma, cov, alpha = 0.95):
    portfolio_mu = np.dot(weight, mu)
    portfolio_sigma = np.sqrt(weight.T @ cov @ weight)
    VaR = (portfolio_mu + norm.ppf(1 - 0.95) * portfolio_sigma) * market_value
    return VaR


def var_hist(market_value, pct_change, weight, alpha = 0.95):
    var_level = pct_change.quantile(1 - alpha)
    VaR = (var_level * market_value) @ weight
    return VaR


def VaR_mc(market_value, mu, sigma, cov, weight, n_sim = 10000, alpha = 0.95):
    random_ret = np.random.multivariate_normal(mu, cov, n_sim)
    portfolio_ret = random_ret @ weight
    var_level = np.quantile(portfolio_ret, 1-alpha)
    VaR = var_level * market_value
    return VaR



