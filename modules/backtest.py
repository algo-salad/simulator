from strategy import Strategy
from portfolio import FakePorfolio
import pandas as pd
from datetime import datetime
from typing import List
from helpers import get_git_root

DATA_ROOT = f'{get_git_root()}/data/'

class Backtest:

    def __init__(self, 
                 start_value, #starting portfolio value
                 datetime_start, 
                 datetime_end, 
                 strategies: List[Strategy]
                 ):
        self.portfolio = FakePorfolio(start_value)
        self.start_value = start_value
        self.strategies = strategies
        self.start = datetime.strptime(datetime_start, '%Y-%m-%d')
        self.end = datetime.strptime(datetime_end, '%Y-%m-%d')
        self.scope = strategies[0].scope
        assert all(strategy.scope == self.scope for strategy in strategies), 'Mixing scopes isnt supported'
        self.tickers = list(set(strategy.ticker for strategy in strategies))
        self.data = self.get_data()
        
    def get_data(self):
        data = None
        for ticker in self.tickers:
            name = f'{ticker}_{self.scope}'
            df = pd.read_csv(f'{DATA_ROOT}/{name}.csv')
            df['Date'] = df['Date'].astype('datetime64')
            df = df[['Date', 'Open']].rename(columns={'Open': f'{ticker}'})
            df = df.loc[(df['Date'] >= self.start) & (df['Date'] <= self.end)].reset_index(drop=True)
            if data is None:
                data = df
            else:
                data = data.merge(df, on='Date', how='inner')
        return data.sort_values('Date')

    def run(self):
        for i in self.data.index:
            dt = self.data.iloc[i]['Date']
            print(f'\n\n{dt}\n\n')
            for strategy in self.strategies:
                price = self.data.iloc[i][strategy.ticker]
                history = self.data.iloc[:i][strategy.ticker].to_list()
                #add other params in here that logic might require
                proportion = strategy.logic(price, history)
                if proportion > 0: 
                    self.portfolio.buy_percent_cash(strategy.ticker, price, proportion)
                else:
                    self.portfolio.sell_percent_value(strategy.ticker, price, -proportion)
        dt = self.data.iloc[-1]['Date']
        out = {}
        portfolio_value = self.portfolio.get_portfolio_value(self.get_prices(dt))
        out['portfolio_value_end'] = portfolio_value
        out['percent'] = (portfolio_value/self.start_value)*100-100
        return out

    def get_prices(self, date):
        row = self.data.loc[self.data['Date'] == date].reset_index(drop=True)
        return {ticker: row.loc[0,ticker] for ticker in self.tickers}

    def print_results(self):
        pass

    def generate_results_visual(self):
        pass



if __name__ == '__main__':

    # price, history, ...

    def fn(current, history, *_):
        if len(history) > 5 and (current > history[-1]):
            return 0.3
        return -1

    b = Backtest(1000, 
                 '2000-01-01', 
                 '2022-01-31', 
                 [Strategy('SPY', 'intraday', fn)])
    print(b.run())