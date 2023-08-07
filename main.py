import requests
import os
from twilio.rest import Client

COMPANY_NAME = "Tesla"
STOCK = "TSLA"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API = os.environ['STOCK_API']

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = os.environ['NEWS_API']

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
MY_TWILIO_NUMBER = os.environ['MY_TWILIO_NUMBER']
MY_PHONE_NUMBER = os.environ['MY_PHONE_NUMBER']

# Find difference in closing stock prices between yesterday and the day
# before yesterday
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "datatype": "json",
    "apikey": STOCK_API
}

response = requests.get(STOCK_ENDPOINT, stock_params)
response.raise_for_status()
stock_data = response.json()['Time Series (Daily)']
stock_data_list = [value for (key, value) in stock_data.items()][:2]

close_value = float(stock_data_list[0]['4. close'])
previous_close_value = float(stock_data_list[1]['4. close'])

difference = close_value - previous_close_value
if difference >= 0:
    diff_direction = "🔺"
else:
    diff_direction = "🔻"
diff_percent = round((difference / previous_close_value) * 100)

# If difference is greater than 5%, get the latest 3 news pieces for the company
if abs(diff_percent) > 0: # TODO Revert value back to 5% after testing
    news_params = {
        "q": COMPANY_NAME,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API
    }

    response = requests.get(NEWS_ENDPOINT, news_params)
    response.raise_for_status()
    news_data = response.json()['articles'][:3]

    formatted_articles = []
    for i in range(3):
        formatted_articles.append(
            f"{STOCK}: {diff_direction}{diff_percent}%\n"
            f"Headline: {news_data[i]['title']}\n"
            f"Brief: {news_data[i]['description']}"
        )

    # Send messages
    client = Client(TWILIO_ACCOUNT_SID , TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=MY_TWILIO_NUMBER,
            to=MY_PHONE_NUMBER
        )
