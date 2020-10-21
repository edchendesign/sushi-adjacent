#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Risk Reduction by Investment Horizon
Created on Wed Oct 21 17:03:45 2020

@author: edchen

Do longer investment horizons reduce variability in outcome? In general,
investment in stocks have a positive expected return, but day-to-day, results
can swing pretty widely. How many trading days should you hold an equity
to minimize these swings? This model measures the coefficient of variation
(standard deviation / mean) for various trading day lags to show the
inflection point of holding days by which risk levels off.

The example below is for the S&P 500 as reported by Yahoo! Finance
and downloaded to the GSPC.csv file
"""

#import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

stock = pd.read_csv('GSPC.csv', sep=',', header=0) #read in 5 years of S&P500 data from Yahoo! Finance
stock.head() #inspect loaded data
len(stock) #1259

#function to create the array of % change in price for a n-day lag
def pct_change(n):
    lagged_changes = []
    try:
        for i in range(len(stock)-n):
            lagged_changes.append(stock['Adj Close'][n+i]/stock['Adj Close'][i]-1)
    except:
        pass
    return lagged_changes

#function to record lag and coefficient of variation related to lag between a and b days (inclusive) where a,b=int and a<b
def cv_by_lag(a,b):
    lag_and_cv = []
    for i in range(b-a+1):
        lag_and_cv.append([a+i,np.std(pct_change(a+i))/np.mean(pct_change(a+i))])
    return lag_and_cv

#generate lags and coefficients of variation for 1-50 days
sp500lag_cv = cv_by_lag(1,50)
sp500lag_cv = np.array(sp500lag_cv) #turn list of lists into sliceable arrays

#plot data
plt.plot(sp500lag_cv[:,0],sp500lag_cv[:,1])
plt.xlabel('lag days')
plt.ylabel('coefficient of variation')
plt.show()



            