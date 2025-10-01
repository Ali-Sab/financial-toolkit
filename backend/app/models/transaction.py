from datetime import date
from app.utils.exchange_rate import get_exchange_rate

class Transaction:
    def __init__(self, date, transaction_type, symbol, amount, currency, exchange_rates, shares=None):
        self.date = date
        self.transaction_type = transaction_type  # BUY, SELL, DIV, TRFIN, TRFOUT, etc.
        self.symbol = symbol  # Stock ticker
        if currency == 'CAD':
            self.amount = float(amount)
        else:
            self.amount = float(amount) * get_exchange_rate(exchange_rates, date)
        self.shares = float(shares) if shares is not None else None

    def is_buy(self):
        return self.transaction_type == 'BUY'
    
    def is_sell(self):
        return self.transaction_type == 'SELL'
    
    def is_dividend(self):
        return self.transaction_type == 'DIV'
    
    def is_interest(self):
        return self.transaction_type == 'FPLINT'
    
    def is_transfer_out(self):
        return self.transaction_type == 'TRFOUT'
    
    def is_transfer_in(self):
        return self.transaction_type == 'TRFIN'
    
    def __str__(self):
        return f"{self.date}: {self.transaction_type} {self.shares} {self.symbol} for {self.amount}"
    
    def __repr__(self):
        return self.__str__()