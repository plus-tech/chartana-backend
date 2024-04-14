import pandas as pd
import env

# App error code range
#
# Information starts with 'I'
# Warning starts with 'W'
# Error starts with 'E'

ISTART: int = 5000
WSTART: int = 6000
ESTART: int = 7000

MSG: dict = {}

IEXIT: int = ISTART
IAPPBEG: int = ISTART + 1
IAPPEND: int = ISTART + 2
IFUNCBEG: int = ISTART + 3
IFUNCEND: int = ISTART + 4
ITICKER: int = ISTART + 5


ECONN: int = ESTART + 1
ESERVER: int = ESTART + 2
ETICKER: int = ESTART + 3

class Msg:
    def __init__(self):
        df = pd.read_csv(env.MSGFILE,
                         index_col=None,
                         header=0,
                         skipinitialspace=True,
                         doublequote=True,
                         low_memory=False
                         )
        global MSG
        MSG = dict(df.values)
