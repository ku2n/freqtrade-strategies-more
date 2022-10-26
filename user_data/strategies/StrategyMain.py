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

    last_profit = -0.02

    # 커스텀
    in_position = True
    side_positive = True # True = 롱, False = 숏

    # 커스텀 스탑로스
    use_custom_stoploss = True

    # Optimal timeframe for the strategy
    timeframe = '1m'

    # Experimental settings (configuration will overide these if set)
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = True

    stoploss = - 0.02

    # Optional order type mapping
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False,
        'stoploss_on_exchange_interval': 60
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
                dataframe.loc[:, 'enter_long'] = 1
            else:
                dataframe.loc[:, 'enter_short'] = 1
            self.in_position = True            

        return dataframe


    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        if self.side_positive == True :
            if (self.last_profit == -0.02) | (self.last_profit == self.stoploss + 0.001) :
                dataframe.loc[:, 'exit_long'] = 1
                if dataframe['exit_long'] == 1 :
                    self.in_position = False
                    self.side_positive = False
        else :
            if (self.last_profit == -0.02) | (self.last_profit == self.stoploss + 0.001) :
                dataframe.loc[:, 'exit_long'] = 1
                if dataframe['exit_long'] == 1 :
                    self.in_position = False
                    self.side_positive = True

        return DataFrame

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:
            
        self.last_profit = current_profit

        if self.in_position : 
            if current_profit < 0.02 :
                return -0.021

            else :
                desired_stoploss = current_profit - 0.021
                return desired_stoploss

        return 1
