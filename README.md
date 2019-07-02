# strategyLearner
# Overview
In this project you will design a learning trading agent. You must draw on the learners you have created so far in the course. Your choices are:

Regression or classification-based learner: Create a strategy using your Random Forest learner. Important note, if you choose this method, you must set the leaf_size for your learner to 5 or greater. This is to avoid degenerate overfitting in-sample. For classification, you must use mode rather than mean (RTLearner, BagLearner).

Reinforcement Learner-based approach: Create a Q-learning-based strategy using your Q-Learner. 

Optimization-based learner: Create a scan-based strategy using an optimizer.
Regardless of your choice above, your learner should work in the following way:

In the training phase (e.g., addEvidence()) your learner will be provided with a stock symbol and a time period. It should use this data to learn a strategy. For instance, for a regression-based learner it will use this data to make predictions about future price changes.
In the testing phase (e.g., testPolicy()) your learner will be provided a symbol and a date range. All learning should be turned OFF during this phase.
You should use exactly the same indicators as in the manual strategy project so we can compare your results. You may optimize your indicators for time (vectorization), but there should be no changes to lookback windows or any other pertinent parameters.
If the date range is the same as used for the training, it is an in-sample test. Otherwise it is an out-of-sample test. Your learner should return a trades dataframe like it did in the last project. Here are some important requirements: Your testPolicy() method should be much faster than your addEvidence() method. The timeout requirements (see rubric) will be set accordingly. Multiple calls to your testPolicy() method should return exactly the same result.

Overall, your tasks for this project include:

Devise numerical/technical indicators to evaluate the state of a stock on each day.
Build a strategy learner based on one of the learners described above that uses the indicators.
Test/debug the strategy learner on specific symbol/time period problems.
Write a report describing your learning strategy.
Scoring for the project will be based on trading strategy test cases and a report.


# Implementation of Strategy Learner

For this part of the project you should develop a learner that can learn a trading policy using your learner. You should be able to use your Q-Learner or RTLearner from the earlier project directly. If you want to use the optimization approach, you will need to create new code or that. You will need to write code in StrategyLearner.py to "wrap" your learner appropriately to frame the trading problem for it.

Your StrategyLearner should implement the following API:

import StrategyLearner as sl
learner = sl.StrategyLearner(verbose = False, impact = 0.000) # constructor
learner.addEvidence(symbol = "AAPL", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) # training phase
df_trades = learner.testPolicy(symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000) # testing phase
The input parameters are:

verbose: if False do not generate any output
impact: The market impact of each transaction.
symbol: the stock symbol to train on
sd: A datetime object that represents the start date
ed: A datetime object that represents the end date
sv: Start value of the portfolio
The output result is:

df_trades: A data frame whose values represent trades for each day. Legal values are +1000.0 indicating a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING. Values of +2000 and -2000 for trades are also legal when switching from long to short or short to long so long as net holdings are constrained to -1000, 0, and 1000.
