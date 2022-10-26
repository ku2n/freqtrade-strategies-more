import logging
from numpy.lib import math
from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import numpy as np
import freqtrade.vendor.qtpylib.indicators as qtpylib

class Chimp(IStrategy):
    INTERFACE_VERSION: int = 3