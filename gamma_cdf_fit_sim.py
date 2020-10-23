#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gamma Fit and Parameter-Based Simulation Model
Created on Thu Oct 22 06:53:50 2020

@author: edchen

What is the probable distribution of price for a given equity in 4 years?
For applications such as option pricing and portfolio risk modeling, we
want to understand more than expected return. In other words, shape matters.

This example fits % price changes in the S&P 500 to a gamma distribution,
then applies that fit to simulate the value of a $100 investment in the S&P 500
in 4 years. A parameterized Monte Carlo approach allows for exploration of
a. how parameters shift with different time slices of data, b. comparison of
parameters across other assets and asset classes, and c. parameter blending
with other similar assets to improve predictive power and model credibility.
"""


#import packages
import numpy as np
import pandas as pd
from scipy.stats import gamma
import matplotlib.pyplot as plt

#generate data
stock = pd.read_csv('GSPC.csv')
stock.head()
pct_chg_11dy = [] #11 day lag means 23 trading intervals per year for 253 trading days
for i in range(len(stock)-11):
    try:
        pct_chg_11dy.append(stock['Adj Close'][i+11]/stock['Adj Close'][i]-1)
    except:
        pass
x = ~np.isnan(pct_chg_11dy) #index nans
pct_chg_11dy = np.array(pct_chg_11dy)[np.array(x)] #remove nans
pct_chg_11dy.sort()
len(pct_chg_11dy) #1248
len(stock) #1259
pct_chg_11dy[0:10]

#fit 11 trading day percentage changes to gamma distribution
gamma.fit(pct_chg_11dy) #parameters generated (282.9305520057203, -0.6432536949289827, 0.0022892728606478552)
fitted_gamma = gamma(282.9305520057203, loc = -0.6432536949289827, scale = 0.0022892728606478552)
x = np.linspace(-.2, .2, 200)
plt.plot(x, fitted_gamma.cdf(x))
plt.xlabel('Fitted Return in 11 Trading Days')
plt.ylabel('Cumulative Probability')
plt.show()

#example of how to to generate gamma random variables (rvs) based on parameterized fit
rvs = fitted_gamma.rvs(size=100)
rvs.sort()
s = np.linspace(0,1,100)
plt.plot(rvs, s)
plt.xlabel('Simulated Return in 11 Trading Days')
plt.ylabel('Cumulative Probability')
plt.show()

#function to perform 1 gamma random walk for y years starting at 100
def gamma_walk(y):
    price = 100
    for i in range(23*y):
        price = price * (1+fitted_gamma.rvs())
    return price

#function to simulate walks n times for y years
def sim_walks(y,n):
    end_prices = []
    for i in range(n):
        end_prices.append(gamma_walk(y))
    return end_prices

#simulate and plot outcomes for price in 4 years with 10000 sims
end_prices = sim_walks(4,10000)
end_prices.sort()
p = np.linspace(0,1,10000)
plt.plot(end_prices,p)
plt.xlim(0,400) #if necessary, set axis dimensions to improve visibility
plt.xlabel('Simulated Value of $100 Invested in 4 Years')
plt.ylabel('Cumulative Probability')
plt.show()

#calculate mean, standard deviation, and 20/50/80th percentiles of the simulation
np.mean(end_prices) #150.59213633393856
np.std(end_prices) #58.131124790544334
end_prices[2000] #102.10388034205951
end_prices[5000] #140.57591888199863
end_prices[8000] #191.73508898383943

