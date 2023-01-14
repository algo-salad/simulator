class Portfolio:
    
    def __init__(self, start_value):
        self.cash = start_value
        self.assets = {}

    def get_portfolio_value(self, prices):
        values = [shares*prices[asset] for asset, shares in self.assets.items()]
        return sum(values) + self.cash

    def buy(self, ticker, price, value):
        if value <= self.cash:
            print(f'BUY ${value} of {ticker}')
            self.cash-=value
            if ticker in self.assets:
                self.assets[ticker]+=value/price
            else:
                self.assets[ticker] = value/price

    def buy_percent_cash(self, ticker, price, proportion):
        value = self.cash * proportion
        self.buy(ticker, price, value)

    def sell(self, ticker, price, value):
        shares = value/price
        if ticker in self.assets and shares <= self.assets[ticker]:
            print(f'Sell ${value} of {ticker}')
            self.assets[ticker]-=shares
            if self.assets[ticker] == 0:
                self.assets.pop(ticker)
            self.cash+=value

    def sell_percent_value(self, ticker, price, proportion):
        if ticker in self.assets:
            value = self.assets[ticker] * proportion * price
            self.sell(ticker, price, value)

class FakePorfolio(Portfolio):
    pass

class RealPortfolio:
    def __init__(self) -> None:
        raise RuntimeError('Not yet implemented')