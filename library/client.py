import pandas as pd
import yfinance as yf
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Payload:
    tickers: str
    period: str = "max"
    end: Optional[datetime] = None
    start: Optional[datetime] = None

    def get_start_as_string(self) -> None | str:
        return self.start.strftime("%Y/%m/%d %H:%M:%S") if self.start else None

    def get_end_as_string(self) -> None | str:
        return self.end.strftime("%Y/%m/%d %H:%M:%S") if self.end else None


class Client:
    __cache: dict[str, pd.DataFrame] = {}

    @staticmethod
    def get(query: Payload) -> pd.DataFrame:
        return yf.download(
            tickers=query.tickers,
            period=query.period,
            start=query.start,
            end=query.end,
            interval="1d",
            group_by="ticker",
        )

    def get_in_cache(self, query: Payload, show_log: bool = False) -> pd.DataFrame:
        # キャッシュがあればそれを使う
        query_hash = str(hash(query))
        if query_hash in self.__cache:
            print('Client use hash: ' + query_hash) if show_log else None
            return self.__cache[query_hash]
        result = self.get(query)
        self.__cache[query_hash] = result
        return result
