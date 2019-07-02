""" 			  		 			     			  	   		   	  			  	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			     			  	   		   	  			  	
Atlanta, Georgia 30332 			  		 			     			  	   		   	  			  	
All Rights Reserved 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Template code for CS 4646/7646 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			     			  	   		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			     			  	   		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			     			  	   		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			     			  	   		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			     			  	   		   	  			  	
or edited. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			     			  	   		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			     			  	   		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			     			  	   		   	  			  	
GT honor code violation. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
-----do not edit anything above this line--- 			  		 			     			  	   		   	  			  	
			  		 			     			  	   		   	  			  	
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
import pandas as pd
import numpy as np 			  		 			     			  	   		   	  			  			  		 			     			  	   		   	  			  			  		 			     			  	   		   	  			  	
import RTLearner as rtl
import BagLearner as bg
from indicators import calculate_sma, calculate_bbp, calculate_momentum
from util import get_data

# +1: LONG
# 0: CASH
# -1: SHORT
# X data - indicators
# Y data - based on N day return (choose N)
# Y values: Use future N day return (not future price).
# Then classify that return as LONG, SHORT or CASH. 
			  		 			     			  	   		   	  			  	
class StrategyLearner(object): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # constructor 			  		 			     			  	   		   	  			  	
    def __init__(self, verbose = False, impact=0.0): 			  		 			     			  	   		   	  			  	
        self.verbose = verbose 			  		 			     			  	   		   	  			  	
        self.impact = impact
        self.bg_learner = self.get_learner()	  		 			     			  	   		   	  			  	
        self.N = 15

    def author(self):
        return "agizatulina3"

    def get_learner(self, learner = rtl.RTLearner, leaf_size = 6, bags = 20, boost = False):
        return bg.BagLearner(learner, kwargs = {"leaf_size": leaf_size}, bags = bags)	 			     			  	   		   	  			  	
    
    def get_indicators_df(self, prices):
        N = self.N
        
        # Calculate indicators
        sma, sma_ratio = calculate_sma(prices, N)
        mtm = calculate_momentum(prices, N) 
        top_band, bot_band, bbp = calculate_bbp(prices, N)

        x_train = np.zeros((len(prices) - N, 3))

        bbp_flat = bbp.as_matrix().flatten()[N:]
        sma_flat = sma_ratio.as_matrix().flatten()[N:]
        mtm_flat = mtm.as_matrix().flatten()[N:]
        
        x_train[: ,0] = bbp_flat
        x_train[: ,1] = sma_flat
        x_train[: ,2] = mtm_flat
         
        # Change Nans to zeros    
        where_nan = np.isnan(x_train)
        x_train[where_nan] = 0
        return x_train

    # this method should create a QLearner, and train it for trading 			  		 			     			  	   		   	  			  	
    def addEvidence(self, symbol = "IBM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), sv = 10000): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
        # add your code to do learning here
        self.symbol = symbol
        impact = self.impact
        N = self.N
	 			     			  	   		   	  			  	
        syms = [symbol] 			  		 			     			  	   		   	  			  	
        dates = pd.date_range(sd, ed) 			  		 			     			  	   		   	  			  	
        prices_all = get_data(syms, dates)  # automatically adds SPY 			  		 			     			  	   		   	  			  	
        prices = prices_all[syms]  # only portfolio symbols 			  		 			     			  	   		   	  			  	
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later 	

        prices = prices.fillna(method = 'ffill').fillna(method = 'bfill')
        self.prices = prices
		  	   		   	  			  	
        if self.verbose: print prices 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
        # example use with new colname 			  		 			     			  	   		   	  			  	
        volume_all = get_data(syms, dates, colname = "Volume")  # automatically adds SPY 			  		 			     			  	   		   	  			  	
        volume = volume_all[syms]  # only portfolio symbols 			  		 			     			  	   		   	  			  	
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later 			  		 			     			  	   		   	  			  	
        if self.verbose: print volume 			  		 			     			  	   		   	  			  	
 		
        # Create X array that has all indicators
        x_train = self.get_indicators_df(prices)

        # Create Y array
        y_train = prices.diff(-1).values.flatten()

        prev = y_train[0]
        
        for i in range(1, len(prices)):
            if y_train[i] == prev:
                y_train[i] = 0
            elif y_train[i] < 0 and y_train[i] > -impact * prices.iloc[i][symbol]:
                y_train[i] = 0
            elif y_train[i] > 0 and y_train[i] < impact * prices.iloc[i][symbol]:
                y_train[i] = 0
            else:
                prev = y_train[i]
                y_train[i] = prev * -1
        
        if self.verbose: print y_train

        self.bg_learner.addEvidence(x_train ,y_train)
	     			  	   		   	  			  	
    # this method should use the existing policy and test it against new data 			  		 			     			  	   		   	  			  	
    def testPolicy(self, symbol = "IBM", sd=dt.datetime(2009,1,1), ed=dt.datetime(2010,1,1), sv = 10000): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
        # here we build a fake set of trades 			  		 			     			  	   		   	  			  	
        # your code should return the same sort of data 			  		 			     			  	   		   	  			  	
        dates = pd.date_range(sd, ed) 			  		 			     			  	   		   	  			  	
        prices_all = get_data([symbol], dates)  # automatically adds SPY 			  		 			     			  	   		   	  			  	
        trades = prices_all[[symbol,]]  # only portfolio symbols 			  		 			     			  	   		   	  			  	
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later 			  		 			     			  	   		   	  			  	
        
        N = self.N

        # Create X array that has all indicators
        x_test = self.get_indicators_df(trades)
        y_test = self.bg_learner.query(x_test)

        if self.verbose: print y_test

        x = 0
        df_trades = pd.DataFrame(0, columns = trades.columns, index = trades.index)
        
        YBUY = 0.5
        YSELL = -0.5
        
        for i in range(0, len(trades) - N):
            if y_test[i] > YBUY:
                if x == 0:
                    x = 1000
                    df_trades[symbol].iloc[i] = 1000
                elif x == -1000:
                    x = 1000
                    df_trades.iloc[i, 0] = 2000
            if y_test[i] < YSELL:
                if x == 0:
                    x = -1000
                    df_trades[symbol].iloc[i] = -1000
                elif x == 1000:
                    x = -1000
                    df_trades[symbol].iloc[i] = -2000
        
        return df_trades		  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
if __name__=="__main__":
    st = StrategyLearner()
    st.addEvidence()	  		 			     			  	   		   	  			  	
    st.testPolicy()	  
