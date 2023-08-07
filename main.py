import requests
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Find difference in closing stock prices between yesterday and the day
# before yesterday
stock_endpoint = "https://www.alphavantage.co/query"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "datatype": "json",
    "apikey": os.environ['STOCK_API']
}

response = requests.get(stock_endpoint, stock_params)
response.raise_for_status()
stock_data = response.json()['Time Series (Daily)']
stock_data_list = [value for (key, value) in stock_data.items()][:2]

close_value = float(stock_data_list[0]['4. close'])
previous_close_value = float(stock_data_list[1]['4. close'])

difference = abs(close_value - previous_close_value)
diff_percent = (difference / previous_close_value) * 100

# TODO If difference is greater than 5%, get the first 3 news pieces for the company
if diff_percent > 5:
    print("Get News")


# TODO Send message with the percentage change and each article's title and link to phone number
# Formatting:
"""
TSLA: 🔺#%
Headline: <headline_name> 
Link: <link>
or
TSLA: 🔻#%
Headline: <headline_name> 
Link: <link>
"""
