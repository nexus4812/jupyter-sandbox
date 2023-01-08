import pandas as pd
import numpy as np
from backtesting import Strategy
from stockstats import StockDataFrame


class BaseStrategy(Strategy):
    def use_macd(self, short: int = 12, long: int = 26, signal: int = 9) -> np.ndarray:
        return self.I(StockDataFrameUtil.macd, self.data.df, short, long, signal)

    def use_average_true_range(self) -> np.ndarray:
        return self.I(StockDataFrameUtil.average_true_range, self.data.df)

    def use_donchian_channel(self, payload: int = 20) -> np.ndarray:
        return self.I(StockDataFrameUtil.donchian_channel, self.data.df, payload)

    def use_simple_moving_average(self, payload: int = 20) -> np.ndarray:
        return self.I(StockDataFrameUtil.simple_moving_average, self.data.df, payload)


class StockDataFrameUtil:
    """
    StockDataFrameから特定のインジケーターを取得するだけのクラス
    """

    @staticmethod
    def __convert_df_to_stock_df(df: pd.DataFrame) -> StockDataFrame:
        sdf = df.copy()
        sdf.rename(
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
        sdf.index.names = ["date"]
        return StockDataFrame(sdf)

    @classmethod
    def macd(
        cls, df: pd.DataFrame, short: int = 12, long: int = 26, signal: int = 9
    ) -> tuple[pd.Series, pd.Series]:
        sdf = cls.__convert_df_to_stock_df(df)

        StockDataFrame.MACD_EMA_SHORT = short
        StockDataFrame.MACD_EMA_LONG = long
        StockDataFrame.MACD_EMA_SIGNAL = signal
        return sdf["macd"], sdf["macds"]

    @classmethod
    def average_true_range(cls, df: pd.DataFrame) -> pd.Series:
        sdf = cls.__convert_df_to_stock_df(df)
        return sdf["atr"]

    @classmethod
    def simple_moving_average(cls, df: pd.DataFrame, payload: int = 20) -> pd.Series:
        sdf = cls.__convert_df_to_stock_df(df)
        return sdf["open_" + str(payload) + "_sma"]

    @classmethod
    def bollinger_bands(
        cls, df: pd.DataFrame, payload: int = 20, std_times: int = 2
    ) -> tuple[pd.Series, pd.Series, pd.Series]:
        sdf = cls.__convert_df_to_stock_df(df)
        sdf.BOLL_PERIOD = payload
        sdf.BOLL_STD_TIMES = std_times
        return sdf["boll"], sdf["boll_ub"], sdf["boll_lb"]

    @classmethod
    def donchian_channel(
        cls, df: pd.DataFrame, payload: int = 20
    ) -> tuple[pd.Series, pd.Series]:
        # 手製すぎるのでどうにかしたい
        count = 0

        max = []
        min = []
        middle = []

        df = cls.__convert_df_to_stock_df(df)
        for index, data in df.iterrows():

            if payload > count:
                # 計算できていない間は反応しないように適当に広げておく
                max.append(data["high"] + 10)
                min.append(data["low"] - 10)
                middle.append((data["high"] + data["low"]) / 2)
                count += 1
                continue

            # 当日は含めないので-1しとく
            range = df[count - payload : count - 1]
            middle.append((range["high"].max() + range["low"].min()) / 2)
            max.append(range["high"].max())
            min.append(range["low"].min())
            count += 1

        df["max"] = max
        df["min"] = min
        # df["middle"] = middle

        return df["min"], df["max"]  # , df["middle"]
