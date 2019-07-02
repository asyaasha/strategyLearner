#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 10:56:30 2019

Student Name: Asiya Gizatulina (replace with your name) 			  		 			     			  	   		   	  			  	

"""

import StrategyLearner as stg
import pandas as pd 			  		 			     			  	   		   	  			  	
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals
from util import get_data

def author():
    return 'agizatulina3'

def modify(trades_df, symbol):
    trades_df['Date'] = trades_df.index
    trades_df['Symbol'] = symbol
    trades_df['Order'] = 'BUY'
    trades_df['Shares'] = trades_df[symbol]
    trades_df.reset_index(drop=True, inplace=True)

    for i in range(0, len(trades_df)):
        if trades_df.iloc[i, 0] < 0:
            amount = trades_df.iloc[i, 4] * -1
            trades_df.iloc[i, 3] = 'SELL'
            trades_df.iloc[i, 4] = amount
    

    return trades_df

def stats(portfolioVal, inp):
    # Calculate stats
    cum_return = portfolioVal.ix[-1] / portfolioVal.ix[0] - 1
    daily_ret = portfolioVal / portfolioVal.shift(1) - 1
    std = daily_ret.std()
    avg = daily_ret.mean()
    
    print 'Input:' + inp
    print 'Portfolio Cumulative: %f' % cum_return
    print 'Portfolio Std of Daily Returns: %f' % std
    print 'Portfolio Mean of Daily Returns: %f' % avg
        
if __name__ == '__main__':
    start = '01-01-2008'
    end = '12-31-2009'
    start_value = 100000
    symbol = 'JPM'

    dates = pd.date_range(start, end)
    prices_all = get_data([symbol], dates)

    learner_str = stg.StrategyLearner(impact = 0.0)
    learner_str.addEvidence(symbol, start, end, start_value)
    trades1 = learner_str.testPolicy(symbol, start, end, start_value)
    trades1 = modify(trades1, symbol)
    
    learner_str = stg.StrategyLearner(impact = 0.04)
    learner_str.addEvidence(symbol, start, end, start_value)
    trades2 = learner_str.testPolicy(symbol, start, end, start_value)
    trades2 = modify(trades2, symbol)
    
    learner_str = stg.StrategyLearner(impact = 0.18)
    learner_str.addEvidence(symbol, start, end, start_value)
    trades3 = learner_str.testPolicy(symbol, start, end, start_value)
    trades3 = modify(trades3, symbol)

    portfolioVal1 = compute_portvals(trades1, start_value)
    portfolioVal2 = compute_portvals(trades2, start_value)
    portfolioVal3 = compute_portvals(trades3, start_value)

    # Normalize
    portfolioVal1 = portfolioVal1 / portfolioVal1.ix[0]
    portfolioVal2 = portfolioVal2 / portfolioVal2.ix[0]
    portfolioVal3 = portfolioVal3 / portfolioVal3.ix[0]
             
    stats(portfolioVal1, '0.0') 
    stats(portfolioVal2, '0.04')
    stats(portfolioVal3, '0.18')
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    portfolioVal1.plot(ax = ax1, color = 'g', linewidth = 1, label='Impact 0.0')
    portfolioVal2.plot(ax = ax1, color = 'r', linewidth = 1, label='Impact 0.04')
    portfolioVal3.plot(ax = ax1, color = 'b', linewidth = 1, label='Impact 0.18')
    
    ax1.set_xlabel('Dates')
     
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.title('Portfolio Values with various Impacts')
    
    # COMENT OUT FOR PLOT
    #plt.show()    
                                 
