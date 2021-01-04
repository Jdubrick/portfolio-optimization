from functions import ticker_info, ticker_price_history, get_stats_data, get_allocation


def main():
    
    # Calling ticker_info() to gather list of ticker symbols from user
    tickers = ticker_info()

    # Calling ticker_price_history() to get 5-year historic price data for tickers and place them into a dateframe
    daily_returns, prices_df = ticker_price_history(tickers)
    
    # Calling get_stats_data() to find equal-weight portfolio statistics, optimal portfolio statistics and optimal weights
    equal_weight_stats, optimal_port_stats, clean_opt_weights = get_stats_data(daily_returns, prices_df, tickers)
    
    # Calling get_allocation() to gather portfolio value amount from user and break portfolio down into # of shares in optimal portfolio
    allocation, leftover = get_allocation(clean_opt_weights, prices_df)

    # Formatting terminal output for user review
    
    print("\nOptimal Portfolio Allocation")
    print("----------------------------\n")
    
    for ticker, shares in allocation.items():
        print("{0}: {1} share(s)".format(ticker, shares))

    print("Funds Remaining: ${0:.2f}".format(leftover))
    
    print("\nOptimal Portfolio Statistics")
    print("----------------------------")

    print("""
Expected Portfolio Return: {0:.2f}%
Portfolio Volatility (risk): {1:.2f}%
Sharpe Ratio: {2:.2f}\n""".format(optimal_port_stats[0] * 100, optimal_port_stats[1] * 100, optimal_port_stats[2]))
    
    for ticker, weight in clean_opt_weights.items():
        print("{0}: {1:.2f}%".format(ticker, weight * 100))
    
    print("\nEqual Weight Portfolio Statistics")
    print("---------------------------------")

    print("""
Expected Portfolio Return: {0:.2f}%
Portfolio Volatility (risk): {1:.2f}%
Sharpe Ratio: {2:.2f}\n""".format(equal_weight_stats[0] * 100, equal_weight_stats[1] * 100, equal_weight_stats[2]))
    
    return tickers


def volatility_change(tickers):
    daily_returns, prices_df = ticker_price_history(tickers)
    
    # Calling get_stats_data() to find equal-weight portfolio statistics, optimal portfolio statistics and optimal weights
    equal_weight_stats, optimal_port_stats, clean_opt_weights = get_stats_data(daily_returns, prices_df, tickers)
    
    # Calling get_allocation() to gather portfolio value amount from user and break portfolio down into # of shares in optimal portfolio
    allocation, leftover = get_allocation(clean_opt_weights, prices_df)

    # Formatting terminal output for user review
    
    print("\nOptimal Portfolio Allocation")
    print("----------------------------\n")
    
    for ticker, shares in allocation.items():
        print("{0}: {1} share(s)".format(ticker, shares))

    print("Funds Remaining: ${0:.2f}".format(leftover))
    
    print("\nOptimal Portfolio Statistics")
    print("----------------------------")

    print("""
Expected Portfolio Return: {0:.2f}%
Portfolio Volatility (risk): {1:.2f}%
Sharpe Ratio: {2:.2f}\n""".format(optimal_port_stats[0] * 100, optimal_port_stats[1] * 100, optimal_port_stats[2]))
    
    for ticker, weight in clean_opt_weights.items():
        print("{0}: {1:.2f}%".format(ticker, weight * 100))
    
    print("\nEqual Weight Portfolio Statistics")
    print("---------------------------------")

    print("""
Expected Portfolio Return: {0:.2f}%
Portfolio Volatility (risk): {1:.2f}%
Sharpe Ratio: {2:.2f}\n""".format(equal_weight_stats[0] * 100, equal_weight_stats[1] * 100, equal_weight_stats[2]))    

# Main function call and loop so that user can keep changing volatility % value without having to re-enter ticker symbols


tickers = main()
answer = input("Do you want to enter a new volatility % value? (Y/N): ")

if answer == 'Y':
    while answer != 'N':
        volatility_change(tickers)
        answer = input("Do you want to enter a new volatility % value? (Y/N): ")
        if answer == 'Y':
            continue
        else:
            print("Shutting down..")
            break
elif answer == 'N':
    print("Shutting down..")
else:
    print("You entered an incorrect answer: ")
    answer = input("Do you want to enter a new volatility % value? (Y/N): ")
    
