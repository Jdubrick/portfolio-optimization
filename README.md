# portfolio-optimization

# Overview
Optimizes a portfolio of securities given a set of ticker symbols

# Libraries:
  pandas
  NumPy
  PyPortfolioOpt
  datetime
  
# Description
User enters ticker symbols as they are listed on Yahoo Finance and the program will compute the portfolio volatility, sharpe ratio, and expected return for that list of securities if they were equal-weighted. The program will then use PyPortfolioOpt and EfficientFrontier to find the optimal portfolio weight for each security that will fall within the users' volatility maximum (max risk willing they are willing to take).

Output is the results from both calculations. The user will be asked for a total dollar value of their portfolio, and using that information and DiscreteAllocation the program will outline how many shares of each security can be purchased to match the weights (price based off closing price of previous day).
