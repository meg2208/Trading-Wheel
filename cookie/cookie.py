

class Cookie:

    def __init__(self, strategies=None):
        self.strategies = strategies
        if strategies:
            self.current_strategy = strategies[0]
        else:
            self.current_strategy = None

