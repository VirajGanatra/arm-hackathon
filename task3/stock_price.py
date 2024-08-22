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



class StockPrice:
    def __init__(self, stock, amount_spent, date_bought):
        self.stock = stock
        self.amount_spent = int(amount_spent)
        self.date_bought = date_bought
        self.session = CachedLimiterSession(
            limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache("yfinance.cache"),
        )

    def calculate_price_difference(self, start_date):
        stock = yf.Ticker(self.stock,  session=self.session)
        stock_history = stock.history(period='max')
        buy_price = stock_history.loc[self.date_bought]['Close']
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_price = stock_history.loc[str(yesterday)]['Close']
        percentage_gain = yesterday_price / buy_price
        new_value = self.amount_spent * percentage_gain
        return new_value - self.amount_spent