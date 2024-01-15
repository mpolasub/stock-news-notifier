import requests
from newsapi import NewsApiClient
from twilio.rest import Client


STOCK = "AAPL"
COMPANY_NAME = "apple"
text = ""

av_endpoint="https://www.alphavantage.co/query"
ALPHA_VANTAGE_KEY=KEY

newsapi = NewsApiClient(api_key=KEY)
news_endpoint = "https://newsapi.org/v2/top-headlines?"

account_sid = ID
auth_token = KEY


av_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_VANTAGE_KEY
}
av_response = requests.get(av_endpoint, av_params)
av_response.raise_for_status()
av_data = av_response.json()

av_days = [key for (key, value) in av_data["Time Series (Daily)"].items()]
price_today = float(av_data["Time Series (Daily)"][av_days[0]]["4. close"])
price_yesterday = float(av_data["Time Series (Daily)"][av_days[1]]["4. close"])


def get_news(arrow, msg, perc):
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    top_headlines = newsapi.get_top_headlines(q=COMPANY_NAME, country="us")
    headline = top_headlines["articles"][0]["title"]
    desc = top_headlines["articles"][0]["content"]

    msg = f"{STOCK}: {arrow}{perc}%\nHeadline: {headline}\nDescription: {desc}"

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='+18443309716',
        body=msg,
        to='+14258372741'
    )
    print(message.status)
    print(msg)


perc_change = 100*(price_today-price_yesterday)/price_yesterday
if perc_change >= 5:
    get_news("🔺", text, perc_change)
elif perc_change <= -5:
    get_news("🔻", text, perc_change)
