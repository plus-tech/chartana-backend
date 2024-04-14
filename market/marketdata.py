import pandas_datareader.data as pdr
import pandas_datareader.nasdaq_trader as pnt

import pandas as pd
import json

import env
from env import Config
import msg
from tools.logging import Logging
from exception.bizexception import BizException

def GetSymbolListImpl():
    """
      Get the list of symbols from the market, NASDAQ.

      :params:
        None
      :returns:
        a list of symbols
    """
    Logging.GetLogger().debug(msg.MSG[msg.IFUNCBEG])
    try:
        if Config.USETESTDATA:
            df = pd.read_csv('.\\testdata\\samplesymbollist.csv',
                             low_memory=False)
        else:
            df = pnt.get_nasdaq_symbols()

        df['id'] = range(1, len(df)+1)
        df = df.fillna(' ')
        columns = {'Nasdaq Traded':     'NasdaqTraded',
                   'Security Name':     'SecurityName',
                   'Listing Exchange':  'ListingExchange',
                   'Market Category':   'MarketCategory',
                   'Round Lot Size':    'RoundLotSize',
                   'Test Issue':        'TestIssue',
                   'Financial Status':  'FinancialStatus',
                   'CQS Symbol':        'CQSSymbol',
                   'NASDAQ Symbol':     'NASDAQSymbol'
        }
        df = df.rename(columns=columns)
        symbols = df.to_dict('records')

    except Exception as e:
        #
        # log an error
        emsg = msg.MSG[msg.ECONN]
        Logging.GetLogger().error(f"{emsg} ({str(e)})")
        symbols = None

    Logging.GetLogger().debug(msg.MSG[msg.IFUNCEND])
    return symbols


def GetSymbolPricesImpl(ticker):
    """
        Get the historical prices of the specified symbol.

        :params:
            code: int, Listed number of the symbol.
        :raises:
            Exceptions during reading data from the market.
        :returns:
            df: DataFrame, symbol's prices
    """

    Logging.GetLogger().debug(msg.MSG[msg.IFUNCBEG])

    prices = None
    try:
        if ticker is None or int(ticker) <= 0:
            emsg = msg.MSG[msg.ETICKER] + f'({ticker})'
            raise BizException(msg.ETICKER, emsg)
        #
        # During test, the datareader gets data from a local csv file
        if Config.USETESTDATA:
            df = pd.read_csv('.\\testdata\\samplestockprice.csv',
                             index_col='Date',
                             parse_dates=True,
                             low_memory=False)
        else:
            Logging.GetLogger().info(msg.MSG[msg.ITICKER].format(ticker))
            df = pdr.DataReader("{}.JP".format(int(ticker)), "stooq").sort_index(ascending=False)

        if df is not None:
            df['Date'] = df.index
            df['id'] = range(1, len(df) + 1)
            prices = df.to_dict('records')

    except BizException as e:
        Logging.GetLogger().error(f"{str(e)}")

    except Exception as e:
        #
        # log an error
        emsg = msg.MSG[msg.ECONN]
        Logging.GetLogger().error(f"{emsg} ({str(e)})")

    Logging.GetLogger().debug(msg.MSG[msg.IFUNCEND])
    return prices
