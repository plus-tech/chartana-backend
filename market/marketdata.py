import pandas_datareader.data as pdr
import pandas_datareader.nasdaq_trader as pnt

import pandas as pd
import numpy as np
import json

import env
from env import Config
import msg
from common.logging import Logging
from exception.bizexception import BizException

def GetSymbolListImpl(fmt=env.DATAFMT.get('DICT')):
    """
      Get the list of symbols from the market, NASDAQ.

      :params:
        fmt: str, indicates the data type of symbols
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

        #
        # Return symbols as a list with the following format.
        #   [['PIII', 'P3 Health Partners Inc. - Class A Common Stock', True, 'Q', 'S', False, 100.0, False, 'N', ' ', 'PIII', False]
        #   ...
        #   ]
        if fmt is not None and fmt.upper() == env.DATAFMT.get('LIST'):
            columns = ['Symbol',
                       'Security Name',
                       'Nasdaq Traded',
                       'Listing Exchange',
                       'Market Category',
                       'ETF',
                       'RoundLotSize',
                       'Test Issue',
                       'Financial Status',
                       'CQS Symbol',
                       'NASDAQ Symbol',
                       'Next Shares'
            ]

            symbols = np.vstack((columns, df[columns].to_numpy())).tolist()

        #
        # Return symbols as a dictionary with the following format.
        #   [
        #     { 'Symbol': 'PIII',
        #       'NasdaqTraded': True,
        #       'SecurityName': 'P3 Health Partners Inc. - Class A Common Stock',
        #       'ListingExchange': 'Q',
        #       'MarketCategory': 'S',
        #       'ETF': False,
        #       'RoundLotSize': 100.0,
        #       'TestIssue': False,
        #       'FinancialStatus': 'N',
        #       'CQSSymbol': ' ',
        #       'NASDAQSymbol': 'PIII',
        #       'NextShares': False,
        #       'id': 7695
        #     },
        #   ...
        #   ]
        else:
            columns = {'NASDAQ Symbol':    'NASDAQSymbol',
                       'Security Name':    'SecurityName',
                       'Nasdaq Traded':    'NasdaqTraded',
                       'Listing Exchange': 'ListingExchange',
                       'Market Category':  'MarketCategory',
                       'Round Lot Size':   'RoundLotSize',
                       'Test Issue':       'TestIssue',
                       'Financial Status': 'FinancialStatus',
                       'CQS Symbol':       'CQSSymbol'
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


def GetSymbolPricesImpl(ticker, fmt=env.DATAFMT.get('DICT')):
    """
        Get the historical prices of the specified symbol.

        :params:
            ticker: int, indicates the listed ticker no.
            fmt: str, indicates the data type of prices
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
            #
            # Return prices as a list with the following format.
            #   [['Date', 'Low', 'Open', 'Close', 'High', 'Volume']
            #   [Timestamp('2024-01-26 00:00:00') 1734.0 1755.0 1748.0 1783.0 405600.0]
            #   ...
            #   ]
            if fmt is not None and fmt.upper() == env.DATAFMT.get('LIST'):
                columns = ['Date', 'Low', 'Open', 'Close', 'High', 'Volume']
                prices = np.vstack((columns, df[columns].to_numpy())).tolist()
            #
            # Return prices as a dictionary with the following format.
            #   [
            #     {
            #         "Close": 1449.0,
            #         "Date": "Mon, 08 Apr 2024 00:00:00 GMT",
            #         "High": 1467.0,
            #         "Low": 1440.0,
            #         "Open": 1451.0,
            #         "Volume": 182200.0,
            #         "id": 1
            #     },
            #   ...
            #   ]
            else:
                prices = df.to_dict('records')

    except BizException as e:
        Logging.GetLogger().error(f"{str(e)}")
        raise e

    except Exception as e:
        #
        # log an error
        emsg = msg.MSG[msg.ECONN]
        Logging.GetLogger().error(f"{emsg} ({str(e)})")
        raise e

    Logging.GetLogger().debug(msg.MSG[msg.IFUNCEND])
    return prices
