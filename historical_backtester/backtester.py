from __future__ import absolute_import, division, print_function, unicode_literals
import yfinance as yf
import os.path
import json
import backtrader as bt
import backtrader.analyzers as btanalyzers
import os


class Backtester:
    def __init__(
        self,
        strategy,
        start_date,
        end_date,
        principle,
        stake,
        commission,
        stock,
    ):
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.principle = principle
        self.stake = stake
        self.commission = commission
        self.stock = stock
        self.info = {
            "name": strategy.__str__(),
            "start_amount": 0,
            "end_amount": 0,
        }

    def fetch_stock_data(self):
        stock_file_path = f"data/{self.stock}.csv"
        if not os.path.exists(stock_file_path):
            print("File not found. Downloading stock data")
            data = yf.download(
                self.stock,
            )
            data.to_csv(stock_file_path)

    def dt_dict_to_normal(self, dict_to_convert):
        new_dict = {}
        for key, value in dict(dict_to_convert).items():
            new_dict[key.strftime("%Y-%m-%d")] = value

        return new_dict

    def backtest(self, should_plot):
        # Get data
        self.fetch_stock_data()

        # Create a cerebro entity
        cerebro = bt.Cerebro()

        # Add the strategy
        cerebro.addstrategy(self.strategy)

        # Datas are in a subfolder of the samples. Need to find where the script is
        # because it could have been called from anywhere
        datapath = os.path.join(os.getcwd(), f"data/{self.stock}.csv")
        print(datapath)

        # Create a Data Feed
        data = bt.feeds.YahooFinanceCSVData(
            dataname=datapath,
            fromdate=self.start_date,
            todate=self.end_date,
            reverse=False,
        )

        # Add the Data Feed to Cerebro
        cerebro.adddata(data)

        # Set our desired cash start
        cerebro.broker.setcash(self.principle)

        # Add a FixedSize sizer according to the stake
        cerebro.addsizer(bt.sizers.FixedSize, stake=self.stake)

        # Set the commission
        cerebro.broker.setcommission(commission=self.commission)

        # Add all strategy analyzers
        analyzers = [
            btanalyzers.AnnualReturn,
            btanalyzers.Calmar,
            btanalyzers.DrawDown,
            btanalyzers.LogReturnsRolling,
            btanalyzers.PeriodStats,
            btanalyzers.PyFolio,
            btanalyzers.Returns,
            btanalyzers.SharpeRatio,
            btanalyzers.SQN,
            btanalyzers.TimeReturn,
            btanalyzers.TradeAnalyzer,
            btanalyzers.Transactions,
            btanalyzers.VWR,
        ]
        for analyzer in analyzers:
            cerebro.addanalyzer(analyzer, _name=analyzer.__name__)

        # Run Cerebro
        print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
        self.info["start_amount"] = cerebro.broker.getvalue()

        strategy_info = cerebro.run()[0]

        print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
        self.info["end_amount"] = cerebro.broker.getvalue()

        self.info["analysis"] = {}

        for analyzer in strategy_info.analyzers._items:
            if type(analyzer).__name__ != "PyFolio":
                self.info["analysis"][type(analyzer).__name__] = analyzer.get_analysis()

        for analyzer in ["Calmar", "LogReturnsRolling", "TimeReturn", "Transactions"]:
            self.info["analysis"][analyzer] = self.dt_dict_to_normal(
                self.info["analysis"][analyzer]
            )

        # Pyfolio stuff

        returns, positions, transactions, gross_lev = (
            strategy_info.analyzers.PyFolio.get_pf_items()
        )

        for df in [returns, positions, transactions, gross_lev]:
            df.index = df.index.strftime("%Y-%m-%d")

        self.info["analysis"]["pyfolio"] = {}
        self.info["analysis"]["pyfolio"]["returns"] = returns.to_dict()
        self.info["analysis"]["pyfolio"]["positions"] = positions.to_dict()
        self.info["analysis"]["pyfolio"]["transactions"] = transactions.to_dict()
        self.info["analysis"]["pyfolio"]["gross_lev"] = gross_lev.to_dict()

        # Store self.info as a json file

        with open(f"logs/models/{self.strategy.__str__()}.json", "w") as f:
            json.dump(self.info, f)

        with open(f"logs/models/{self.strategy.__str__()}_Simple.json", "w") as f:
            simple_dict = self.info.copy()
            del simple_dict["analysis"]
            simple_dict["num_of_trades"] = self.info["analysis"]["TradeAnalyzer"][
                "total"
            ]["closed"]
            json.dump(simple_dict, f)

        if should_plot:
            cerebro.plot()
