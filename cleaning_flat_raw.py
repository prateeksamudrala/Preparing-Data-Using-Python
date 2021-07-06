# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 20:55:04 2021

@author: Jyothi Samudrala
"""
# Raw Dump. Can use optimization/cleanup

import pandas as pd
import matplotlib.pyplot as plt


bitcoin_df = pd.read_csv("coin_Bitcoin.csv")
bitcoin_df.head(10)

# Replace Headers
bitcoin_df_renamed = bitcoin_df.rename(columns={"SNo": "sno", "Name": "currency", "Symbol": "symbol", "Date": "date_time", "High": "high_price_usd", "Low": "low_price_usd", "Open": "open_price_usd", "Close": "close_price_usd", "Volume": "trade_volume_usd", "Marketcap": "marketcap_usd" })

# Checking size
bitcoin_df.shape
# 2862 Rows, 10 Columns

# Checking size of new df
bitcoin_df_renamed.shape
# 2862 Rows, 10 Columns

# Subsetting original dataset to ONLY relevant columns.
bitcoin_df_subset = bitcoin_df_renamed[['currency','date_time','high_price_usd','low_price_usd','open_price_usd','close_price_usd','trade_volume_usd','marketcap_usd']]
bitcoin_df_subset.head(10)

# Checking size of new df
bitcoin_df_subset.shape
# 2862 Rows, 8 Columns

# Plotting a histogram of all variables

for col in bitcoin_df_subset.columns:
    plt.title('Plot of '+ col)
    plt.hist(bitcoin_df_subset[col],bins=25)
    plt.grid()
    plt.show()
    
# Descriptive stats
bitcoin_df_subset.describe()

# Checking null values
bitcoin_df_subset.isnull().sum()
# There are no missing values

# Unique values - checking for duplicate issues - in bitcoin_df_subset

column_names =['currency','date_time', 'high_price_usd', 'low_price_usd', 'open_price_usd', 'close_price_usd', 'trade_volume_usd', 'marketcap_usd']
for v in column_names:
    unique_values = bitcoin_df_subset[v].unique()
    unique_values_num = bitcoin_df_subset[v].nunique()
    print("There are {} unique values in '{}'. They are: {}".format(unique_values_num,v,unique_values))
    print()

# Fortunately, we don't have any duplicates dates and other cryptocurrencies, besides bitcoin.
 
# The rest of the columns are expected to NOT have unique values

# Subsetting dataframe further, to remove rows where 
# high_price_usd, low_price_usd, open_price_usd, close_price_usd, trade_volume_usd and marketcap_usd are ZERO.

bitcoin_df_subset_high = bitcoin_df_subset[(bitcoin_df_subset['high_price_usd'] != 0)]
bitcoin_df_subset_high.shape
# 2862 rows and 8 columns. Indicating there are no ZERO values in high_price_usd

bitcoin_df_subset_low = bitcoin_df_subset[(bitcoin_df_subset['low_price_usd'] != 0)]
bitcoin_df_subset_low.shape
# 2862 rows and 8 columns. Indicating there are no ZERO values in low_price_usd

bitcoin_df_subset_open = bitcoin_df_subset[(bitcoin_df_subset['open_price_usd'] != 0)]
bitcoin_df_subset_open.shape
# 2862 rows and 8 columns. Indicating there are no ZERO values in open_price_usd

bitcoin_df_subset_trade = bitcoin_df_subset[(bitcoin_df_subset['trade_volume_usd'] != 0)]
bitcoin_df_subset_trade.shape
# 2620 rows and 8 columns. trade_volume_usd had 242 rows with ZEROs.

bitcoin_df_subset_market = bitcoin_df_subset[(bitcoin_df_subset['marketcap_usd'] != 0)]
bitcoin_df_subset_market.shape
# 2862 rows and 8 columns. Indicating there are no ZERO values in marketcap_usd

# So final dataset should be the dataset we got from removing rows where trade_volume_usd was ZERO

bitcoin_df_subset_final = bitcoin_df_subset_trade
bitcoin_df_subset_final.shape
# 2620 rows and 8 columns

# Checking for outliers and data quality on high_price_usd, low_price_usd, open_price_usd, close_price_usd, trade_volume_usd, and marketcap_usd
# Scatter plots
plt.scatter((bitcoin_df_subset_final['high_price_usd']), bitcoin_df_subset_final['low_price_usd'], c='purple')
plt.xlabel("High Price Per the Day")
plt.ylabel("Low Price Per the Day")
plt.grid()
plt.title("Scatter Plot between High price vs Low price to see extreme variations")

# There are no extreme variations in price between high and low. Meaning, there are no outliers in high price and low price for the timeline


plt.scatter((bitcoin_df_subset_final['open_price_usd']), bitcoin_df_subset_final['close_price_usd'], c='green')
plt.xlabel("Open Price Per the Day")
plt.ylabel("Close Price Per the Day")
plt.grid()
plt.title("Scatter Plot between Open price vs Close price to see extreme variations")

# There are no extreme variations in price between open and close

plt.boxplot(bitcoin_df_subset_final.trade_volume_usd, notch=True)
# The boxplot shows one outlier for trade_volume at 3.5 some value. So, we will remove this value in our new subset.

bitcoin_df_subset_final = bitcoin_df_subset_final[(bitcoin_df_subset['trade_volume_usd'] < 3.509679e+11)] # got this value from max in descriptive statistics
bitcoin_df_subset_final.shape
# 2619 rows and 8 columns. The one value has been removed.

plt.boxplot(bitcoin_df_subset_final.marketcap_usd, notch=True)

bitcoin_df_subset_final.shape
# The box plot shows several values outside of the "box". But, considering bitcoin market capitalization has grown siginificantly 
# only in recent years. We won't be removing any "outlying" values here.