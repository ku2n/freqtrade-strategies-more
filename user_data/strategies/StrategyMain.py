# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from datetime import datetime, timedelta
from freqtrade.persistence import Trade


class StrategyMain(IStrategy):
    INTERFACE_VERSION: int = 3

    # 커스텀
    in_position = False
    side_positive = True # True = 롱, False = 숏

    # 커스텀 스탑로스
    use_custom_stoploss = True

    # Optimal timeframe for the strategy
    timeframe = '1m'

    # run "populate_indicators" only for new candle
    process_only_new_candles = False

    # Experimental settings (configuration will overide these if set)
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = True

    # Optional order type mapping
    order_types = {
        'entry': 'limit',
        'exit': 'limit'
    }

    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        heikinashi = qtpylib.heikinashi(dataframe)
        dataframe['ha_open'] = heikinashi['open']
        dataframe['ha_close'] = heikinashi['close']
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        if not self.in_position:
            if self.side_positive:
                dataframe.loc[(), 'enter_long'] = True
            else:
                dataframe.loc[(), 'enter_short'] = True
            self.in_position = True            

        return dataframe


    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return DataFrame

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:
            

        self.in_position = False
        if self.side_positive:
            self.side_positive = False
        else:
            self.side_positive = True

        if current_profit < 0.02:

            return -0.02 # return a value bigger than the initial stoploss to keep using the initial stoploss

            # After reaching the desired offset, allow the stoploss to trail by half the profit
        desired_stoploss = current_profit - 0.02

            # Use a minimum of 2.5% and a maximum of 5%
        return desired_stoploss
