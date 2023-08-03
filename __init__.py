

# Import trading ranges class
from TradeRanges.trade_rangesV2 import TradeRanges



def __init__():
    ticker = "RIVN"
    tr = TradeRanges(ticker, months=3, data_source="Yahoo")
    tr.plot_graph()

__init__()