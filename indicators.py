#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 15:56:03 2019
code that implements your indicators as functions 
that operate on dataframes. The "main" code in 
indicators.py should generate the charts that illustrate 
your indicators in the report.
Student Name: Asiya Gizatulina (replace with your name) 			  		 			     			  	   		   	  			  	
	
"""

import pandas as pd 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  			  		 			     			  	   		   	  			  			  		 			     			  	   		   	  			  	
from util import get_data 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

		  		 			     			  	   		   	  			  	
def author():
    return 'agizatulina3'

def calculate_sma(price, lookback): # Simple Moving Average
    sma = price.rolling(window = lookback, min_periods = lookback).mean()
    ratio = price / sma

    return sma, ratio
    
		  		 			     			  	   		   	  			  	
def calculate_bbp(price, lookback): # Bollinger Bands
    sma = calculate_sma(price, lookback)[0]

    rolling_std = price.rolling(window = lookback, min_periods = lookback).std()
    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    
    bbp = (price - bottom_band) / (top_band - bottom_band)

    return top_band, bottom_band, bbp

def calculate_momentum(price, lookback): #Momentum
    mtm = price.copy()
    lookback = lookback * 2
    
    mtm.values[lookback:, :] = mtm.values[lookback:, :] / mtm.values[:-lookback:, :] - 1
    mtm.values[:lookback,:]= np.nan
    
    return mtm

def plot_momentum(price, lookback):
    mtm = calculate_momentum(price, lookback)   
    fig = plt.figure(constrained_layout=True)
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 11
    fig_size[1] = 9
    G = gridspec.GridSpec(2, 2, figure = fig)
    
    axes_1 = fig.add_subplot(G[0, :])
    axes_1.plot(price, color = 'm', linewidth = '0.4', label='Price')
    axes_1.margins(x = 0)
    axes_1.grid(linewidth=0.5)
    axes_1.set_ylabel('Price', size='13', labelpad=22)
    axes_1.legend(loc='lower left')
    axes_1.set_title('JPM Momentum', size='16', pad=20)

    axes_2 = fig.add_subplot(G[-1, :])
    axes_2.plot(mtm, color = 'c', label = 'Ratio', linewidth = '0.6')
    axes_2.margins(x = 0)
    axes_2.set_title('Momentum', color = 'c')
    axes_2.set_xlabel('Date', size='13', labelpad=20)
    axes_2.set_ylabel('Momentum', size='13')
    plt.xticks(rotation = 70)
    plt.grid(linewidth=0.5)
    plt.tight_layout()
    plt.show()
    
def plot_sma(price, lookback):
    sma, ratio = calculate_sma(price, lookback)
    
    fig = plt.figure(constrained_layout=True)
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 11
    fig_size[1] = 9
    G = gridspec.GridSpec(3, 3, figure = fig)
    
    axes_1 = fig.add_subplot(G[:-1, :])
    axes_1.plot(sma, color = 'y', linestyle='dashed', label='SMA')
    axes_1.plot(price, color = 'm', linewidth = '0.4', label='Price')
    axes_1.margins(x = 0)
    axes_1.grid(linewidth=0.5)
    axes_1.set_ylabel('Price', size='13', labelpad=22)
    axes_1.legend(loc='lower left')
    axes_1.set_title('JPM Simple Moving Average', size='16', pad=20)

    axes_2 = fig.add_subplot(G[-1, :])
    axes_2.plot(ratio, color = 'c', label = 'Ratio', linewidth = '0.6')
    axes_2.margins(x = 0)
    axes_2.set_title('Price to SMA ratio', color = 'c')
    axes_2.set_xlabel('Date', size='13', labelpad=20)
    axes_2.set_ylabel('Price to SMA ratio', size='13')
    plt.xticks(rotation = 70)
    plt.grid(linewidth=0.5)
    plt.tight_layout()
    plt.show()
    
def plot_bbp(price, lookback):
    top_band, bot_band, bbp = calculate_bbp(price, lookback)
    sma = calculate_sma(price, lookback)[0]

    fig = plt.figure(constrained_layout=True)
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 11
    fig_size[1] = 9
    G = gridspec.GridSpec(3, 3, figure = fig)
     
    axes_1 = fig.add_subplot(G[:-1, :])
    axes_1.plot(sma, color = 'y', linestyle='dashed', label='SMA')
    axes_1.plot(price, color = 'c', linewidth = '0.4', label='Price')
    axes_1.plot(top_band, linewidth = '0.6', color = 'm', label='Top bb')
    axes_1.plot(bot_band, linewidth = '0.6', color = 'r', label='Bottom bb')
    axes_1.margins(x = 0)
    axes_1.grid(linewidth=0.5)
    axes_1.set_ylabel('Price', size='13', labelpad=22)
    axes_1.legend(loc='lower left')
    axes_1.set_title('JPM Bollinger Bands', size='16', pad=20)

    axes_2 = fig.add_subplot(G[-1, :])
    axes_2.plot(bbp, color = 'c', label = 'BBP', linewidth = '0.6')
    axes_2.margins(x = 0)
    axes_2.set_title('BBP', color = 'c')
    axes_2.set_xlabel('Date', size='13', labelpad=20)
    axes_2.set_ylabel('Percentage %', size='13')
    plt.xticks(rotation = 70)
    plt.grid(linewidth=0.5)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    dates = pd.date_range('01-01-2008', '12-31-2009') 			  		 			     			  	   		   	  			  	
    price = get_data(['JPM'], dates).drop(['SPY'], axis=1)

    # UNCOMMENT TO SHOW PLOTS
    #plot_sma(price, 20)
    #plot_bbp(price, 20)
    #plot_momentum(price, 20)
