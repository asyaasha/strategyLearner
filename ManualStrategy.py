#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 15:57:16 2019
Code implementing a ManualStrategy object (your manual strategy).
It should implement testPolicy() which returns a trades data 
frame (see below). The main part of this code should call 
marketsimcode as necessary to generate the plots used in the 
report.
 
The in sample/development period is January 1, 2008 to December 31 2009.
The out of sample/testing period is January 1, 2010 to December 31 2011.
Starting cash is $100,000.
Allowable positions are: 1000 shares long, 1000 shares short, 0 shares.
Transaction costs for ManualStrategy: Commission: $9.95, Impact: 0.005.
Student Name: Asiya Gizatulina (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: agizatulina3 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 903387961 (replace with your GT ID) 	
"""

import pandas as pd 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  			  		 			     			  	   		   	  			  	
from util import get_data
from indicators import calculate_sma, calculate_bbp, calculate_momentum
from marketsimcode import compute_portvals 		 			     			  	   		   	  			  	
import matplotlib.pyplot as plt
		  		 			     			  	   		   	  			  	
class ManualStrategy(object):
   def __init__(self):
       pass

   def author():
       return 'agizatulina3'
   
   def testPolicy(self, sym = 'JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000):
       lookback = 20
       shares = 1000
       
     
       dates = pd.date_range(sd, ed)
       price = get_data([sym], dates).drop(['SPY'], axis=1)
       price = price.fillna(method='ffill') 
       price = price.fillna(method='bfill')
       
       # debugg
       pd.set_option('display.max_rows', 1000)
       
       sma, sma_ratio = calculate_sma(price, lookback)
       mtm = calculate_momentum(price, lookback) 
       top_band, bot_band, bbp = calculate_bbp(price, lookback)
       
       orders1 = []

       for day in range(lookback + 1, price.shape[0]):
          if (sma_ratio.iloc[day][sym] < 0.95) and (bbp.iloc[day][sym] < 0) and (mtm.iloc[day][sym] < -0.095):
              orders1.append([price.index[day].date(), sym, 'BUY', shares])
          elif sma_ratio.iloc[day][sym] > 1.05 and bbp.iloc[day][sym] > 1 and (mtm.iloc[day][sym] > 0.095):
              orders1.append([price.index[day].date(), sym, 'SELL', shares])
          elif (mtm.iloc[day][sym] > 0.095) & (mtm.iloc[day][sym] > -0.095): 
              orders1.append([price.index[day].date(), sym, 'BUY', 0])

       df_trades = pd.DataFrame(orders1, columns=['Date', 'Symbol', 'Order', 'Shares'])  

       return df_trades
   
   def plot(self, val1, val2, name, title):
       fig = plt.figure()
       ax1 = fig.add_subplot(111)

       colorPort = 'r'
       colorBench ='g'
           
       val1.plot(ax = ax1, color = colorPort, linewidth = 1, label='Manual Strategy')
       val2.plot(ax = ax1, color = colorBench, linewidth = 1, label='Strategy Learner')
       ax1.set_ylabel('Portfolio Value')
       ax1.set_xlabel('Date')
     

       plt.grid(True)
    
       plt.legend(loc='upper left')
       plt.title(title)

       plt.show()
       fig.clf()
       plt.close(fig)

   def get_bench(self, trades):
       benchmark = trades.copy()
       benchmark.iloc[0]['Order'] = 'BUY'
       benchmark.iloc[0]['Shares'] = 1000
       benchmark.iloc[1:]['Order'] = 'BUY'
       benchmark.iloc[1:]['Shares'] = 0
      
       return benchmark

if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
    ms = ManualStrategy()
    start_value = 100000
    sym = 'JPM'

    start = '01-01-2008'
    end = '12-31-2009'
    
    startOut = '01-01-2010'
    endOut = '12-31-2011'


    trades = ms.testPolicy(sym, start, end, start_value)
    buying = trades[trades['Order']=='BUY']
    selling = trades[trades['Order']=='SELL']
    longTrades = buying[buying['Shares'] == 1000]
    shortTrades = selling[selling['Shares'] == 1000]
    
    # get benchmark values
    benchmark = ms.get_bench(trades)

    # get portfolio values
    portfolioVal = compute_portvals(trades, start_val = start_value)
    benchmarkVal = compute_portvals(benchmark, start_val = start_value)

    # Normalize
    portfolioVal = portfolioVal / portfolioVal.ix[0]
    benchmarkVal = benchmarkVal / benchmarkVal.ix[0]
    
    # UNCOMMENT TO SHOW PLOT
    # PLOT IN Sample
    #ms.plot(portfolioVal, benchmarkVal, longTrades, shortTrades, 'insample.pdf', 'JPM Manual Strategy - In Sample')

    
    # Plot out of sample
    tradesOut = ms.testPolicy(sym, startOut, endOut, start_value)
    benchmarkOut = ms.get_bench(tradesOut)
    
    # get portfolio values
    portfolioOut = compute_portvals(tradesOut, start_val=start_value)
    benchmarkOut = compute_portvals(benchmarkOut, start_val=start_value)

    portfolioOut = portfolioOut / portfolioOut.ix[0]
    benchmarkOut = benchmarkOut / benchmarkOut.ix[0]
    
    # UNCOMMENT TO SHOW PLOT
    # PLOT OUT Sample
    #ms.plot(portfolioOut, benchmarkOut, False, False, 'outsample.pdf', 'JPM Manual Strategy - Out Sample')

    
    port_val = start_value * portfolioVal
    cum_return = portfolioVal.ix[-1] / portfolioVal.ix[0] - 1
    daily_ret = portfolioVal / portfolioVal.shift(1) - 1
    std = daily_ret.std()
    avg = daily_ret.mean()
    
    print 'Portfolio Cumulative: %f' % cum_return
    print 'Portfolio Std of Daily Returns: %f' % std
    print 'Portfolio Mean of Daily Returns: %f' % avg
    
    port_val = start_value * benchmarkVal
    cum_return = benchmarkVal.ix[-1] / benchmarkVal.ix[0] - 1
    daily_ret = benchmarkVal / benchmarkVal.shift(1) - 1
    std = daily_ret.std()
    avg = daily_ret.mean()
    
    print 'Benchmark Cumulative: %f' % cum_return
    print 'Benchmark Std of Daily Returns: %f' % std
    print 'Benchmark Mean of Daily Returns: %f' % avg

    port_val = start_value * portfolioOut
    cum_return = portfolioOut.ix[-1] / portfolioOut.ix[0] - 1
    daily_ret = portfolioOut / portfolioOut.shift(1) - 1
    std = daily_ret.std()
    avg = daily_ret.mean()
    
    print 'Portfolio Out Cumulative: %f' % cum_return
    print 'Portfolio Out Std of Daily Returns: %f' % std
    print 'Portfolio Out Mean of Daily Returns: %f' % avg
    
    port_val = start_value * benchmarkOut
    cum_return = benchmarkOut.ix[-1] / benchmarkOut.ix[0] - 1
    daily_ret = benchmarkOut / benchmarkOut.shift(1) - 1
    std = daily_ret.std()
    avg = daily_ret.mean()
    
    print 'Benchmark Out Cumulative: %f' % cum_return
    print 'Benchmark Out Std of Daily Returns: %f' % std
    print 'Benchmark Out Mean of Daily Returns: %f' % avg