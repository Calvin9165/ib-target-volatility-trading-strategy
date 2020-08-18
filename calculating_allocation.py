
from gathering_data import sorted_df, lookback_period
from math import sqrt

target_vol = 0.15 / len(sorted_df.columns)

tickerDict = {}

for ticker in sorted_df:

    # calculate the annualized volatility for each stock based on the
    # past n (lookback_period) days
    ticker_vol = (sorted_df[ticker].pct_change()).std() * sqrt(252)

    # create a dictionary that has key as ticker name
    # first value is most recent closing price
    # second value is the % allocation the ticker should be in the portfolio
    tickerDict.update({ticker: (sorted_df[ticker][-1], target_vol / ticker_vol)})


if __name__ == '__main__':

    for key, value in tickerDict.items():

        print('{} has an annualized volatility of {} and therefore we are allocating {} of the portfolio'
              .format(key, round(target_vol / value[1], 2), round(value[1], 2)))

    print(tickerDict)

