from .strategy import Strategy
from backtrader.indicators import SimpleMovingAverage


class SMAStrategy(Strategy):
    def __init__(self):
        super().__init__()

        # Variables
        self.close = self.datas[0].close

        # Indicators
        self.sma = SimpleMovingAverage(self.close, period=15)

    def process_data(self):
        # Check if we are in the market
        if not self.position:
            if self.close[0] > self.sma[0]:

                # Buy
                self.log("BUY CREATE, %.2f" % self.close[0])
                self.order = self.buy()

        else:
            if self.close[0] < self.sma[0]:
                # Sell
                self.log("SELL CREATE, %.2f" % self.close[0])
                self.order = self.sell()

    def __str__():
        return "SMA Strategy"
