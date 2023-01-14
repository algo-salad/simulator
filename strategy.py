from typing import Callable
from inspect import signature, Parameter

class Strategy:
    
    def __init__(self, ticker, scope, execute: Callable[...,float]):
        self.ticker = ticker
        self.scope = scope
        assert any(p.kind == Parameter.VAR_POSITIONAL for p in signature(execute).parameters.values()), 'execute function must accepts variable *args'
        self.execute = execute