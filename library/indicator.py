import pandas as pd
from stockstats import StockDataFrame


class Indicator:
    def __init__(self, stock_data_frame: StockDataFrame):
        self.stock_data_frame = stock_data_frame

    def __copy(self) -> StockDataFrame:
        return self.stock_data_frame.__copy()

    def get_stock_data_frame(self):
        return self.__copy()

    def macd(
        self, short: int = 12, long: int = 26, signal: int = 9
    ) -> tuple[pd.Series, pd.Series]:
        sdf = self.__copy()
        StockDataFrame.MACD_EMA_SHORT = short
        StockDataFrame.MACD_EMA_LONG = long
        StockDataFrame.MACD_EMA_SIGNAL = signal
        return sdf["macd"], sdf["macds"]

    def average_true_range(self) -> pd.Series:
        sdf = self.__copy()
        return sdf["atr"]

    def simple_moving_average(self, payload: int = 20) -> pd.Series:
        sdf = self.__copy()
        return sdf["open_" + str(payload) + "_sma"]

    def bollinger_bands(
        self, payload: int = 20, std_times: int = 2
    ) -> tuple[pd.Series, pd.Series, pd.Series]:
        sdf = self.__copy()
        sdf.BOLL_PERIOD = payload
        sdf.BOLL_STD_TIMES = std_times
        return sdf["boll"], sdf["boll_ub"], sdf["boll_lb"]

    def donchian_channel(self, payload: int = 20) -> tuple[pd.Series, pd.Series]:
        sdf = self.__copy()
        return sdf["max_-" + str(payload) + "~-1"], sdf["min_-" + str(payload) + "~-1"]
