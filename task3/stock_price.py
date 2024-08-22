import datetime
import yfinance as yf
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
import numpy as np
import pandas as pd

STOCK_BOUGHT = 'TSLA'
AMOUNT_SPENT = 100.0
DATE_BOUGHT = datetime.date(2024, 7, 1)

# Make a cache to reduce spamming yahoo!
class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)

stock = yf.Ticker(STOCK_BOUGHT,  session=session)

# Get stock info
stock_history = stock.history(period='max')

print(str(DATE_BOUGHT))
buy_price = stock_history.loc[str(DATE_BOUGHT)]['Close']

# Get price yesterday as API does not provide
# live data for today
yesterday = datetime.date.today() - datetime.timedelta(days=1)
yesterday_price = stock_history.loc[str(yesterday)]['Close']

# Calculate change in price
percentage_gain = yesterday_price / buy_price
new_value = AMOUNT_SPENT * percentage_gain
print(f"New price: {new_value}")
print(f"Profit: {new_value - AMOUNT_SPENT}")