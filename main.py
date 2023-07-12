import requests
import time
# token from https://www.tiingo.com/documentation/end-of-day
from local import TOKEN

def get_stock_data(ticker: str, period: str):
    date = get_historical_date_by_period(period)
    historical_price = get_stock_price_by_date(ticker, date)
    current_price = get_stock_price_by_date(ticker)
    price_change = get_price_change(historical_price, current_price)
    percent = get_formatted_price_change_string(price_change)
    return historical_price, current_price, percent


def get_historical_date_by_period(period: str):
    # period in days
    seconds = time.time()
    # how many seconds passed since the beginning of the epoch
    now = time.localtime(seconds - period*24*3600)
    # maybe - 3*3600 because of the time zone
    year = time.strftime("%Y", now)
    month = time.strftime("%m", now)
    day = time.strftime("%d", now)
    date = '{}-{}-{}'.format(year, month, day)
    return date


def get_stock_price_by_date(ticker: str, date: str = None) -> float:
    if not date:
        seconds = time.time()
        # how many seconds passed since the beginning of the epoch
        now = time.localtime(seconds-24*3600)
        date = time.strftime("%Y-%m-%d", now)
    result = requests.get(("https://api.tiingo.com/tiingo/daily/{}/" +
                           "prices?startDate={}&token={}").format(ticker, date, TOKEN))
    return result.json()[0]['adjClose']


def get_price_change(historical_price: float, current_price: float) -> float:
    price_change = (current_price - historical_price)/historical_price*100
    return price_change


def get_formatted_price_change_string(price_change: float) -> str:
    if price_change > 0:
        percent = "+%.2f" % (price_change)
    else:
        percent = "%.2f" % (price_change)
    percent += "%"
    return percent


print(get_stock_data('MSFT', 365))
