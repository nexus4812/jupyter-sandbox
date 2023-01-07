import pandas as pd
import yfinance as yf
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Payload:
    tickers: str
    period: str | None
    start: datetime | None
    end: datetime | None

    def get_start_as_string(self) -> None | str:
        if self.start:
            return self.start.strftime("%Y-%m-%d %H:%M:%S")
        return None

    def get_end_as_string(self) -> None | str:
        if self.end:
            return self.end.strftime("%Y-%m-%d %H:%M:%S")
        return None

    def get_period(self) -> None | str:
        if self.period:
            return self.period
        return None


class Client:
    @staticmethod
    def get(query: Payload) -> pd.DataFrame:
        return yf.download(
            tickers=query.tickers,
            period=query.get_period(),
            start=query.get_start_as_string(),
            end=query.get_end_as_string(),
            interval="1d",
            group_by="ticker",
        )
