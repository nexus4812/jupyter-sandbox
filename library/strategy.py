import pandas as pd
import numpy as np
from backtesting import Strategy
from stockstats import StockDataFrame
from backtesting.lib import crossover


class BaseStrategy(Strategy):
    def declare_macd(self, short: int = 12, long: int = 26, signal: int = 9) -> np.ndarray:
        return self.I(StockDataFrameUtil.macd, self.data.df, short, long, signal)

    def declare_average_true_range(self) -> np.ndarray:
        return self.I(StockDataFrameUtil.average_true_range, self.data.df)

    def declare_donchian_channel(self, payload: int = 20) -> np.ndarray:
        return self.I(StockDataFrameUtil.donchian_channel, self.data.df, payload)

    def declare_simple_moving_average(self, payload: int = 20) -> np.ndarray:
        return self.I(StockDataFrameUtil.simple_moving_average, self.data.df, payload)


class ConcreateStrategy(BaseStrategy):
    # 神クラスパターンだが、Backtesting.py自体がこの作りなので致し方なし
    prop_macd_short = 12
    prop_macd_long = 26
    prop_macd_signal = 9

    prop_donchian_channel = 20

    def use_macd_strategy(self):
        self.macd, self.macd_signal = self.declare_macd(self.prop_macd_short, self.prop_macd_long, self.prop_macd_signal)

    def macd_golden_cross(self):
        self.__assert_attribute(['macd', 'macd_signal'])
        return crossover(self.macd, self.macd_signal)

    def macd_dead_cross(self):
        self.__assert_attribute(['macd', 'macd_signal'])
        return crossover(self.macd_signal, self.macd)

    def use_donchian_channel(self):
        self.dc_max, self.dc_min = self.declare_donchian_channel()

    def is_donchian_channel_updated_highest(self):
        self.__assert_attribute(['dc_max'])
        return self.data.High[-1] > self.dc_max[-1]

    def is_donchian_channel_updated_lowest(self):
        self.__assert_attribute(['dc_min'])
        return self.data.Low[-1] > self.dc_min[-1]

    def __assert_attribute(self, attributes: list[str]):
        # 呼び出し順序が存在する良くないクラス設計なので、簡単にチェックしとく
        for attribute in attributes:
            if not self.__has_attribute(attribute):
                raise AttributeError("has undefined attributes: " + attribute)

    def __has_attribute(self, attribute: str) -> bool:
        return getattr(self, attribute, False) != False

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
            range = df[count - payload: count - 1]
            middle.append((range["high"].max() + range["low"].min()) / 2)
            max.append(range["high"].max())
            min.append(range["low"].min())
            count += 1

        df["max"] = max
        df["min"] = min
        # df["middle"] = middle

        return df["min"], df["max"]  # , df["middle"]
