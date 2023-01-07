from lib.client import Payload
from lib.repository import Repository

print(
    Repository.get_indicator(Payload(tickers="spy", start=None, end=None, period=None))
)
