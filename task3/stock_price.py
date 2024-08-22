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



class Stock:
    def __init__(self, stock):
        self.stock = stock
        self.session = CachedLimiterSession(
            limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache("yfinance.cache"),
        )

    def stock_history(self):
        stock = yf.Ticker(self.stock,  session=self.session)
        stock_history = stock.history(period='max')
        return stock_history

    def calculate_price_difference(self, amount_spent, date_bought):
        stock_history = self.stock_history()
        buy_price = stock_history.loc[date_bought]['Close']
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_price = stock_history.loc[str(yesterday)]['Close']
        percentage_gain = yesterday_price / buy_price
        new_value = amount_spent * percentage_gain
        return new_value - amount_spent