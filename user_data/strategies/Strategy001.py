
# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class Strategy001(IStrategy):
    N = 1

    """
    Strategy 001
    author@: Gerald Lonlas
    github@: https://github.com/freqtrade/freqtrade-strategies

    How to use it?
    > python3 ./freqtrade/main.py -s Strategy001
    """

    INTERFACE_VERSION: int = 3
    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    """
    minimal_roi = {
        "60":  0.01,
        "30":  0.03,
        "20":  0.04,
        "0":  0.05
    }
    """

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.02

    # Optimal timeframe for the strategy
    timeframe = '5m'

    # trailing stoploss
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.0 # 이건 보니까 최소 몇 퍼센트 올라와야지 그때부터 스탑로스가 걸리게 하는 거 인듯

    # run "populate_indicators" only for new candle
    process_only_new_candles = False

    # Experimental settings (configuration will overide these if set)
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = True

    # Optional order type mapping
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',  # 이거 entry 가격으로 바꿔야함
        'stoploss_on_exchange': False
    }

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        """

        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)

        heikinashi = qtpylib.heikinashi(dataframe)
        dataframe['ha_open'] = heikinashi['open']
        dataframe['ha_close'] = heikinashi['close']

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column

        (2022/10/19) {
            File "/home/kun/freqtrade-strategies-more/user_data/strategies/Strategy001.py", line 105, in populate_entry_trend
                if(N % 2 == 0) :
            UnboundLocalError: local variable 'N' referenced before assignment
            
            class 변수를 glboal 변수처럼 사용했기 때문 에러.
            N을 self.N으로 바꿔서 해결했음.
        }

        (2022/10/19) {
            File "/home/kun/freqtrade/.env/lib/python3.9/site-packages/pandas/core/indexing.py", line 2581, in convert_missing_indexer
            raise KeyError("cannot use a single bool to index into setitem")

            pandas.loc[True, "something"]에서 모두 고를때 True, False는 안먹히는듯.
            pandas.loc[(), "something"]로 바꿔서 해결했음.
        }
        """

        if(self.N % 2 == 0) :
            dataframe.loc[(), 'enter_long'] = 1
            self.N += 1
        
        else :
            dataframe.loc[(), 'enter_short'] = 1
            self.N += 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        
        dataframe.loc[
            (
                qtpylib.crossed_above(dataframe['ema50'], dataframe['ema100']) &
                (dataframe['ha_close'] < dataframe['ema20']) &
                (dataframe['ha_open'] > dataframe['ha_close'])  # red bar
            ),
            'exit_long'] = 1

        dataframe.loc[
            (

            ),
            'exit_short'] = 1

        return dataframe
        """
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe


"""
(2022/10/19) {
    OperationalException: `populate_exit_trend` or `populate_sell_trend` must be implemented.
    무조건 선언해두라고 해서 야매로 선언해두었음
}
"""
            