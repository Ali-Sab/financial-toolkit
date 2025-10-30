class StockPosition:
    def __init__(self, symbol):
        self.symbol = symbol
        self.total_cost = 0
        self.total_shares = 0
        
    def buy(self, shares, cost):
        self.total_cost = round(self.total_cost + abs(cost), 8)
        self.total_shares = round(self.total_shares + shares, 8)
        
    def sell(self, shares):
        if shares > self.total_shares:
            raise ValueError(f"Cannot sell {shares} shares of {self.symbol} when only {self.total_shares} are owned")
        
        # Calculate cost basis for sold shares
        average_cost = self.total_cost / self.total_shares
        cost_basis = average_cost * shares
        
        # Update position
        self.total_cost = round(self.total_cost - cost_basis, 8)
        self.total_shares = round(self.total_shares - shares, 8)
        
        return cost_basis