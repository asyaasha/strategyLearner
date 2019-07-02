#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 15:56:50 2019
improved version of your marketsim code that accepts a "trades" 
data frame (instead of a file). More info on the trades data 
frame below. It is OK not to submit this file if you have 
subsumed its functionality into one of your other required 
code files.
@author: a
"""

import pandas as pd 			  		 			     			  	   		   	  			  			  		 			     			  	   		   	  			  	
from util import get_data 
			  		 			     			  	   		   	  			  	
def author():
    return 'agizatulina3'
		  		 			     			  	   		   	  			  	
def compute_portvals(orders, start_val = 100000, commission = 9.95, impact = 0.005): 			  		 			     			  	   		   	  			  	
    ordersTable = orders
    ordersTable.sort_values(by='Date')	

    # List of stocks
    stocksList = ordersTable['Symbol'].unique().tolist()
    
    # First and last dates
    startDate = ordersTable['Date'].iloc[0];
    endDate = ordersTable['Date'].iloc[-1];

    #dates = pd.DataFrame(index = pd.date_range(startDate, endDate))
    pricesTable = get_data(stocksList, pd.date_range(startDate, endDate))

    # Fill missing data
    pricesTable.fillna(method = 'ffill',inplace = True)
    pricesTable.fillna(method = 'backfill', inplace = True)

    cash = [1] * (pricesTable.size)
    CASH = 'Cash'
    pricesTable[CASH] = 1 
 
    tradesTable = pricesTable.copy()
    tradesTable[stocksList] = 0

    tradesTable['Cash'] = 0
    tradesTable = tradesTable * 0.0
    tradesTable['Cash'][0] = start_val


    for i, b in enumerate(ordersTable.index):
        
        Date = ordersTable.Date[i]
        
        SYM = ordersTable.Symbol[i]
        share = ordersTable.Shares[i]

        price = pricesTable[SYM][Date]


        if ordersTable.Order[i]  == 'SELL':
            cash = share * price
   
        else:
             cash = share * -price

        # Add orders to trades table
        tradesTable[CASH][Date] = tradesTable[CASH][Date] - share * price * impact - commission + cash

        if ordersTable.Order[i] == 'SELL':
            share = share * -1

        tradesTable[SYM][Date] = tradesTable[SYM][Date] + share


    for i in range(1, tradesTable.shape[0]):
        for y in range(0, tradesTable.shape[1]):
            tradesTable.iloc[i,y] += tradesTable.iloc[i-1,y]

    valuesTable = pricesTable.mul(tradesTable)

    portfolioValues = valuesTable.sum(axis=1)
      	   		   	  			  	
    return portfolioValues

if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
    print ''