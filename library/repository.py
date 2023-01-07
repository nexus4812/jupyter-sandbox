from stockstats import StockDataFrame
from .client import Client, Payload
from .indicator import Indicator


class Repository:
    @staticmethod
    def get_indicator(query: Payload) -> Indicator:
        df = Client.get(query)

        df.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "amount",
                "Volume": "volume",
            },
            inplace=True,
        )
        df.index.names = ["date"]
        return Indicator(StockDataFrame(df))
