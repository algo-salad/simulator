from modules.backtest import Backtest
from modules.strategy import Strategy

def test_run():
    # price, history, ...
    def generate_lookback(num, step=1):
        def fn(current, history, *_):
            p = current
            if len(history) > num:
                good = True
                for i in range(1,num+1,step):
                    if p > history[-i]:
                        p = history[-i]
                    else:
                        good = False
                        break
                if good:
                    return 0.3
            return -1
        return fn

    b = Backtest('2000-01-01', '2022-01-31', [Strategy('SPY', 'intraday', generate_lookback(10,2))])
    print(b.run())

if __name__ == '__main__':
    test_run()