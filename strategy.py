from typing import Callable, TypedDict, List

class Strategy:
    
    def __init__(self, ticker, scope, execute: Callable[...,float]):
        self.ticker = ticker
        self.scope = scope
        self.execute = execute