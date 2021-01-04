import datetime
from pandas_datareader import data as web
from pypfopt import risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt.efficient_frontier import EfficientFrontier
import numpy as np
import pandas as pd


def ticker_info():
    '''
    Asks users to enter ticker symbols of stocks in their portfolio 
    '''
    
    stock_entry = input("Enter ticker symbol exactly as it is on Yahoo Finance (Enter 'Done' to close): ")
    tickers = []
    while stock_entry != 'Done':
        tickers.append(stock_entry)
        stock_entry = input("Enter ticker symbol exactly as it is on Yahoo Finance (Enter 'Done' to close): ")

    return tickers


def ticker_price_history(tickers):
    '''
    Takes the list of tickers and gathers the last 5 years of historic closing price data, returns df of daily returns for each ticker symbol
    '''
    
    prices_df = pd.DataFrame()
    
    for stock in tickers:
        prices_df[stock] = web.DataReader(stock, data_source='yahoo', start='01/01/2015', end=datetime.date.today())['Adj Close']

    daily_returns = prices_df.pct_change()

    return daily_returns, prices_df


def get_stats_data(daily_returns, prices_df, tickers):
    '''
    Computes for equal weight: covariance, portfolio variance, portfolio volatility, annual portfolio return (equal weights)
    Compute optimal portfolio: expected returns, portfolio volatility & max sharpe ratio obtainable within the given volatility parameters using efficient frontier 
    '''
    
    # Asks user for risk aversion
    target_volatility = float(input("Enter your target volatility value (Decimal): "))
    
    # Using the average of 252 for total number of trading days in a year for covariance matrix
    annual_cov_matrix = daily_returns.cov() * 252
    
    # As user was not asked to input weights, we will use equal weighting to find initial portfolio variance
    weights_per = 1 / len(tickers)
    weights_list = []
    
    for _ in range(len(tickers)):
        weights_list.append(weights_per)
    
    weights_list = np.array(weights_list)
    
    portfolio_variance = np.dot(weights_list.T, np.dot(annual_cov_matrix, weights_list))
    
    # Calculating portfolio volatility (squareroot of variance)
    portfolio_volatility = np.sqrt(portfolio_variance)

    # Calculating annual portfolio return with equal weights
    portfolio_annual_return_equal = np.sum(daily_returns.mean() * weights_list * 252)
    
    # Calculating Sharpe Ratio for Equal-Weight portfolio (0.02 risk-free is to match the default risk-free rate of pypfopt efficient frontier)
    equal_sharpe = (portfolio_annual_return_equal - 0.02) / portfolio_volatility
    
    # Organizing all the statistics for the equal weighted, non optimized portfolio
    equal_weight_stats = [portfolio_annual_return_equal, portfolio_volatility, equal_sharpe]
    
    # Calculating the expected returns and sample covariance using PyPortfolioOpt library
    exp_annual_returns = expected_returns.mean_historical_return(prices_df)
    sample_cov = risk_models.sample_cov(prices_df)
    
    # Optimizing Sharpe ratio (risk-adjusted return) using Efficient Frontier (risk-free rate defaulted to 2%)
    # TANGENT PORTFOLIO
    efficient_frontier = EfficientFrontier(exp_annual_returns, sample_cov)
    
    while True:
        try:
            raw_opt_weights = efficient_frontier.efficient_risk(target_volatility)
            break
        except ValueError:
            target_volatility = float(input("You entered a risk value too low for those given securities, enter a new one: "))
        except:
            target_volatility = float(input("You entered a risk value too low for those given securities, enter a new one: "))
    clean_opt_weights = efficient_frontier.clean_weights()
    optimal_port_stats = efficient_frontier.portfolio_performance(verbose=False)

    return equal_weight_stats, optimal_port_stats, clean_opt_weights


def get_allocation(clean_opt_weights, prices_df):
    '''
    Determines the dollar ($) amount of each stock you can purchase today to match determined weights
    will also give a leftover dollar ($) amount if there is not enough to buy a whole share
    '''
    
    # Gather user input for dollar ($) amount of portfolio
    port_value = float(input("Please enter the total dollar ($) amount you have for your portfolio: $"))
    
    latest_prices = get_latest_prices(prices_df)
    discrete_alloc = DiscreteAllocation(clean_opt_weights, latest_prices, total_portfolio_value=port_value)
    allocation, leftover = discrete_alloc.lp_portfolio(verbose=False)
    
    return allocation, leftover
