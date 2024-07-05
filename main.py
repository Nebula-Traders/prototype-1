from strategies.SMA_strategy import SMAStrategy
from historical_backtester.backtester import Backtester
import datetime
import json


import argparse


def main(
    strategy, start_date, end_date, principle, stake, commission, stock, should_plot
):
    backtester = Backtester(
        strategy, start_date, end_date, principle, stake, commission, stock
    )
    backtester.backtest(should_plot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", type=str, required=True)
    parser.add_argument("--start_date", type=str, required=True)
    parser.add_argument("--end_date", type=str, required=True)
    parser.add_argument("--principle", type=float, default=1000.0)
    parser.add_argument("--stake", type=int, default=10)
    parser.add_argument("--commission", type=float, default=0.01)
    parser.add_argument("--stock", type=str, required=True)
    parser.add_argument("--plot", type=str, required=True)
    args = parser.parse_args()

    strategy = None

    if args.strategy == "SMA":
        strategy = SMAStrategy

    main(
        strategy,
        datetime.datetime.strptime(args.start_date, "%Y-%m-%d"),
        datetime.datetime.strptime(args.end_date, "%Y-%m-%d"),
        args.principle,
        args.stake,
        args.commission,
        args.stock,
        args.plot == "True",
    )
