import pandas as pd
import norgatedata
from datetime import datetime

lookback_period = 60
end_date = datetime.now()


watchlistname = 'spy_tlt_gld'
symbols = norgatedata.watchlist_symbols(watchlistname)

df_list = []

for symbol in symbols:

    norgate_df = norgatedata.price_timeseries(
        symbol,
        end_date=end_date,
        limit=lookback_period,
        interval='D',
        format='pandas-dataframe')

    # creating a symbol column so that we can identify
    # what ticker information we're looking at
    norgate_df['Symbol'] = symbol

    # appending the dataframes to an empty list to concatenate them after the for loop
    df_list.append(norgate_df)


# joins the dataframes together for all tickers
appended_data = pd.concat(df_list)

# just keep the closing data and the symbol
appended_data.drop(['Open', 'High', 'Low', 'Volume', 'Turnover',
                    'Unadjusted Close', 'Dividend'], axis=1, inplace=True)


portfolio_tickers = [i for i in appended_data['Symbol'].unique()]

df_dict = {}


for i in portfolio_tickers:
    df_data = appended_data['Close'][appended_data['Symbol'] == i]
    df_dict.update({i: df_data})


sorted_df = pd.DataFrame(df_dict)

if __name__ == '__main__':
    print(sorted_df)