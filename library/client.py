import pandas as pd
import yfinance as yf
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Payload:
    tickers: str
    period: str = 'max'
    end:  Optional[datetime] = None
    start: Optional[datetime] = None

    def get_start_as_string(self) -> None | str:
        return self.start.strftime("%Y-%m-%d %H:%M:%S") if self.start else None

    def get_end_as_string(self) -> None | str:
        return self.end.strftime("%Y-%m-%d %H:%M:%S") if self.end else None


class Client:
    @staticmethod
    def get(query: Payload) -> pd.DataFrame:
        return yf.download(
            tickers=query.tickers,
            period=query.period,
            start=query.get_start_as_string(),
            end=query.get_end_as_string(),
            interval="1d",
            group_by="ticker",
        )
