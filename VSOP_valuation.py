#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monte-Carlo Approach to VSOP Valuation
Created on Thu Oct 15 14:20:07 2020

@author: edchen

What is the option value of the right to buy shares in a company on a future date
at the current price? The code below simulates the value of the stock on that future date
based on randomly selected observed daily price % changes, then discounts the difference
in that future value vs. the strike price when greater than 0 to calculate a present value
of the option as a mean and shows the %ile spread of simulated outcomes.

The example below is for 100 units of the S&P 500 as reported by Yahoo! Finance
and downloaded to the GSPC.csv file
"""

#import packages
import numpy as np
import pandas as pd

#read in exported csv from Yahoo! Finance
stock = pd.read_csv('GSPC.csv', sep=',', header=0) #example uses last 5 years of S&P 500
stock.head(8) #check to see if data has been read in correctly

#define parameters
trading_days_per_year = 253
vesting_years = 4 
discount_rate = 0.1 #set based on your time value of money
shares_granted = 100 #set based on your offer
strike_price = 3512 #set based on last trade close in this example
start_price = 3512 #set based on last trade close in this example
vol_scalar = 1 #daily % change scale factor
drop_top_n = 0 #drop n highest %change days (if you want to be conservative)
drop_bottom_n = 0 #drop n lowest %change days (if you're aggressive)

#calculate daily % change in closing price
pct_chg = []
for i in range(len(stock['Adj Close'])-1):
    try:
        pct_chg.append((stock['Adj Close'][i+1]-stock['Adj Close'][i])/stock['Adj Close'][i])
    except:
        pct_chg.append(0)
x = ~np.isnan(pct_chg)
pct_chg = np.array(pct_chg)[np.array(x)]
pct_chg.sort()
pct_chg = pct_chg[0+drop_bottom_n:len(pct_chg)-drop_top_n]

#check results
pct_chg[0:10]
min(pct_chg)
max(pct_chg)
len(pct_chg)
np.percentile(pct_chg,90)
(1+sum(pct_chg)/len(pct_chg))**253-1 #implied expected annual return

#function to return ending price given random walk based on parameters
def end_price(pct_chg):
    current_price = start_price
    for i in range(trading_days_per_year*vesting_years):
        current_price = current_price*(1+np.random.choice(pct_chg)*vol_scalar)
    return current_price

#check one simulation
end_price(pct_chg)

#function to price shares granted with n simulations
def vsop_value(simulations):
    values = []
    for i in range(simulations):
        x = end_price(pct_chg)
        if x > strike_price:
            values.append(x-strike_price)
        else:
            values.append(0)
    print('mean: ',round((shares_granted*sum(values)/len(values))/(1+discount_rate)**vesting_years,0),'\r\n'
          '10th %ile: ',round(shares_granted*np.percentile(values,10)/(1+discount_rate)**vesting_years,0),'\r\n'
          '20th %ile: ',round(shares_granted*np.percentile(values,20)/(1+discount_rate)**vesting_years,0),'\r\n'
          '30th %ile: ',round(shares_granted*np.percentile(values,30)/(1+discount_rate)**vesting_years,0),'\r\n'
          '40th %ile: ',round(shares_granted*np.percentile(values,40)/(1+discount_rate)**vesting_years,0),'\r\n'
          '50th %ile: ',round(shares_granted*np.percentile(values,50)/(1+discount_rate)**vesting_years,0),'\r\n'
          '60th %ile: ',round(shares_granted*np.percentile(values,60)/(1+discount_rate)**vesting_years,0),'\r\n'
          '70th %ile: ',round(shares_granted*np.percentile(values,70)/(1+discount_rate)**vesting_years,0),'\r\n'
          '80th %ile: ',round(shares_granted*np.percentile(values,80)/(1+discount_rate)**vesting_years,0),'\r\n'
          '90th %ile: ',round(shares_granted*np.percentile(values,90)/(1+discount_rate)**vesting_years,0),'\r\n'
          '95th %ile: ',round(shares_granted*np.percentile(values,95)/(1+discount_rate)**vesting_years,0),'\r\n'
          '99th %ile: ',round(shares_granted*np.percentile(values,99)/(1+discount_rate)**vesting_years,0))

#find the average present value of 10000 simulations
vsop_value(10000)
"""
mean:  165270.0 
10th %ile:  0.0 
20th %ile:  29202.0 
30th %ile:  62878.0 
40th %ile:  97304.0 
50th %ile:  131038.0 
60th %ile:  169575.0 
70th %ile:  214968.0 
80th %ile:  275127.0 
90th %ile:  371557.0 
95th %ile:  452797.0 
99th %ile:  673208.0
"""




