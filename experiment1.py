#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Student Name: Asiya Gizatulina (replace with your name) 			  		 			     			  	   		   	  			  	

"""

import ManualStrategy as mst
import StrategyLearner as stg
from marketsimcode import compute_portvals			  		 			     			  	   		   	  			  	
import numpy as np 	
import random

def author():
    return 'agizatulina3'

if __name__ == '__main__':
    random.seed(300)
    np.random.seed(300)
    start_value = 100000
    
    start = '01-01-2008'
    end = '12-31-2009'
    
    symbol = 'JPM'

    manual_str = mst.ManualStrategy()
    learner_str = stg.StrategyLearner()

    learner_str.addEvidence(symbol, start, end, start_value)

    manual_trades = manual_str.testPolicy(symbol, start, end, start_value)
    learner_trades = learner_str.testPolicy(symbol, start, end, start_value)
    
    # Modify to make it work with compute_portvals
    learner_trades['Date'] = learner_trades.index
    learner_trades['Symbol'] = symbol
    learner_trades['Order'] = 'BUY'
    learner_trades['Shares'] = learner_trades[symbol]
    learner_trades.reset_index(drop = True, inplace = True)

    learner_df = learner_trades.copy()

    for i in range(0, len(learner_df)):
        if learner_df.iloc[i, 0] < 0:
            amount = learner_df.iloc[i, 4] * -1
            learner_df.iloc[i, 3] = 'SELL'
            learner_df.iloc[i, 4] = amount

    # Print learner_trades
    # Get portfolio values
    manualVal = compute_portvals(manual_trades, start_val = start_value)
    learnerVal = compute_portvals(learner_df, start_val = start_value)
     
    # Normalize
    manualVal = manualVal / manualVal.ix[0]
    learnerVal = learnerVal / learnerVal.ix[0]

    # COMMENT OUT FOR PLOT
    # Plot
    manual_str.plot(manualVal, learnerVal, 'experiment1.pdf', 'Manual Strategy vs Learner Strategy')
     
    # Calculate stats manual
    port_val = start_value * manualVal
    cum_return = manualVal.ix[-1] / manualVal.ix[0] - 1
    daily_ret = manualVal / manualVal.shift(1) - 1
    std = daily_ret.std()
    avg = daily_ret.mean()
     
    print 'Manual Strategy Portfolio Cumulative: %f' % cum_return
    print 'Manual Strategy Portfolio Std of Daily Returns: %f' % std
    print 'Manual Strategy Portfolio Mean of Daily Returns: %f' % avg
    
    # Calculate stats learner
    port_val = start_value * learnerVal
    cum_return = learnerVal.ix[-1] / learnerVal.ix[0] - 1
    daily_ret = learnerVal / learnerVal.shift(1) - 1
    std = daily_ret.std()
    avg = daily_ret.mean()
     
    print 'Strategy Learner Portfolio Cumulative: %f' % cum_return
    print 'Strategy Learner Portfolio Std of Daily Returns: %f' % std
    print 'Strategy Learner Portfolio Mean of Daily Returns: %f' % avg

