from modules.backtest import Backtest
from modules.strategy import Strategy

def test_run():
    # price, history, ...
    def fn(current, history, *_):
        if len(history) > 5 and (current > history[-1]):
            return 0.3
        return -1

    b = Backtest('2000-01-01', '2022-01-31', [Strategy('SPY', 'intraday', fn)])
    print(b.run())

if __name__ == '__main__':
    test_run()