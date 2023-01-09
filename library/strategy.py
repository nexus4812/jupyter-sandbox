import pandas as pd
import numpy as np
from backtesting import Strategy
from stockstats import StockDataFrame
from backtesting.lib import crossover


class BaseStrategy(Strategy):
    def declare_macd(
        self, short: int = 12, long: int = 26, signal: int = 9
    ) -> np.ndarray:
        return self.I(StockDataFrameUtil.macd, self.data.df, short, long, signal)

    def declare_atr(self) -> np.ndarray:
        return self.I(StockDataFrameUtil.atr, self.data.df)

    def declare_donchian_channel(self, period: int = 20) -> np.ndarray:
        return self.I(StockDataFrameUtil.donchian_channel, self.data.df, period)

    def declare_sma(self, period: int = 20) -> np.ndarray:
        return self.I(StockDataFrameUtil.sma, self.data.df, period)


class ConcreateStrategy(BaseStrategy):
    # 神クラスパターンだが、Backtesting.py自体がこの作りなので致し方なし

    # macd
    prop_macd_short: int = 12
    prop_macd_long: int = 26
    prop_macd_signal: int = 9

    # DC
    prop_donchian_channel_period: int = 20

    # atr
    prop_atr_stop_loss: float = 2.0
    prop_atr_take_profit: float = 2.0

    # sma
    prop_sma_period: int = 20

    def use_macd(self):
        self.macd, self.macd_signal = self.declare_macd(
            self.prop_macd_short, self.prop_macd_long, self.prop_macd_signal
        )

    def is_macd_golden_cross(self) -> bool:
        self.__assert_attribute(["macd", "macd_signal"])
        return crossover(self.macd, self.macd_signal)

    def is_macd_dead_cross(self) -> bool:
        self.__assert_attribute(["macd", "macd_signal"])
        return crossover(self.macd_signal, self.macd)

    def use_donchian_channel(self):
        self.dc_max, self.dc_min = self.declare_donchian_channel(
            self.prop_donchian_channel_period
        )

    def is_donchian_channel_updated_highest(self):
        self.__assert_attribute(["dc_max"])
        return self.data.High[-1] > self.dc_max[-1]

    def is_donchian_channel_updated_lowest(self):
        self.__assert_attribute(["dc_min"])
        return self.data.Low[-1] < self.dc_min[-1]

    def use_atr(self) -> None:
        self.atr = self.declare_atr()

    def get_stop_loss_price_by_atr(self) -> float:
        """
        ATR基準による損切り価格を取得する
        例) prop_atr_stop_loss = 1.00
        現在価格 - 1ATRで損切り
        :return: 損切りする金額
        """
        self.__assert_attribute(["atr"])
        return self.data.Close[-1] - self.atr[-1] * self.prop_atr_stop_loss

    def get_take_profit_price_by_atr(self) -> float:
        """
        ATR基準による利確価格を取得する
        例) prop_atr_take_profit = 1.00
        現在価格 + 1ATRで利確
        :return: 利確する金額
        """
        self.__assert_attribute(["atr"])
        return self.data.Close[-1] + self.atr[-1] * self.prop_atr_take_profit

    def buy_with_atr(self):
        """
        ATRによる損切り、利確価格を設定した上で購入する
        """
        self.buy(
            sl=self.get_stop_loss_price_by_atr(),
            tp=self.get_take_profit_price_by_atr(),
        )

    def use_sma(self):
        self.sma = self.declare_sma(self.prop_sma_period)

    def is_price_higher_than_sma(self) -> bool:
        self.__assert_attribute(["sma"])
        return self.sma[-1] < self.data.High[-1]

    def is_price_lower_than_sma(self) -> bool:
        self.__assert_attribute(["sma"])
        return self.sma[-1] > self.data.Low[-1]

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
    def atr(cls, df: pd.DataFrame) -> pd.Series:
        sdf = cls.__convert_df_to_stock_df(df)
        return sdf["atr"]

    @classmethod
    def sma(cls, df: pd.DataFrame, period: int = 20) -> pd.Series:
        sdf = cls.__convert_df_to_stock_df(df)
        return sdf["open_" + str(period) + "_sma"]

    @classmethod
    def bollinger_bands(
        cls, df: pd.DataFrame, period: int = 20, std_times: int = 2
    ) -> tuple[pd.Series, pd.Series, pd.Series]:
        sdf = cls.__convert_df_to_stock_df(df)
        sdf.BOLL_PERIOD = period
        sdf.BOLL_STD_TIMES = std_times
        return sdf["boll"], sdf["boll_ub"], sdf["boll_lb"]

    @classmethod
    def donchian_channel(
        cls, df: pd.DataFrame, period: int = 20
    ) -> tuple[pd.Series, pd.Series]:
        # 手製すぎるのでどうにかしたい
        count = 0

        max = []
        min = []
        middle = []

        df = cls.__convert_df_to_stock_df(df)
        for index, data in df.iterrows():

            if period > count:
                # 計算できていない間は反応しないように適当に広げておく
                max.append(data["high"] + 10)
                min.append(data["low"] - 10)
                middle.append((data["high"] + data["low"]) / 2)
                count += 1
                continue

            # 当日は含めないので-1しとく
            range = df[count - period : count - 1]
            middle.append((range["high"].max() + range["low"].min()) / 2)
            max.append(range["high"].max())
            min.append(range["low"].min())
            count += 1

        df["max"] = max
        df["min"] = min
        # df["middle"] = middle

        return df["min"], df["max"]  # , df["middle"]
