import logging
from typing import List, Dict, Any
from app.models.stock_position import StockPosition

def calculate_yearly_net_profit(transactions):
    """Calculate net profit from transactions by year."""
    yearly_net_profit = []
    stock_positions = {}  # Dictionary of StockPosition objects
    adjusted_cost_basis_sells = []

    for transaction in transactions:
        year = int(transaction.date.year)
        symbol = transaction.symbol
        amount = transaction.amount
        shares = transaction.shares

        # Skip if shares is None (like for dividends)
        if shares is None:
            continue

        if transaction.transaction_type == 'SELL':
            if symbol not in stock_positions:
                logging.error(f"{symbol} SOLD BEFORE BUY on {transaction.date}.")
                continue
                
            try:
                # Use the StockPosition.sell method to calculate cost basis
                cost = stock_positions[symbol].sell(shares)
                profit = amount - cost
                adjusted_cost_basis_sells.append({
                    'stock': symbol, 
                    'year': year, 
                    'shares': shares, 
                    'profit': profit, 
                    'proceeds': amount, 
                    'adjusted_cost': cost
                })
                
                # Find existing year entry or create new one
                year_entry = next((item for item in yearly_net_profit if item['year'] == year and item['stock'] == symbol), None)
                if year_entry:
                    year_entry['net_profit'] = round(year_entry['net_profit'] + profit, 2)
                else:
                    yearly_net_profit.append({'year': year, 'stock': symbol, 'net_profit': round(profit, 2)})
            except ValueError as e:
                logging.warning(f"{e} on {transaction.date}")
        elif transaction.transaction_type == 'BUY':
            if symbol not in stock_positions:
                stock_positions[symbol] = StockPosition(symbol)
            stock_positions[symbol].buy(shares, amount)

    return yearly_net_profit, adjusted_cost_basis_sells

def calculate_yearly_dividends_awarded(dividends):
    """Calculate dividends awarded from DIV transactions by stock and year."""
    yearly_dividends = []

    for dividend in dividends:
        year = int(dividend.date.year)
        stock = dividend.symbol
        amount = dividend.amount

        # Find existing year/stock entry or create new one
        entry_match = next((item for item in yearly_dividends if item['year'] == year and item['stock'] == stock), None)
        if entry_match:
            entry_match['dividends'] = round(entry_match['dividends'] + amount, 2)
        else:
            yearly_dividends.append({'year': year, 'stock': stock, 'dividends': amount})

    return yearly_dividends

def calculate_yearly_interest_earned(interest):
    """Calculate interest earned from FPLINT transactions by year."""
    yearly_interest = []
    
    for entry in interest:
        year = int(entry.date.year)
        amount = entry.amount
        
        # Find existing year entry or create new one
        year_entry = next((item for item in yearly_interest if item['year'] == year), None)
        if year_entry:
            year_entry['interest'] = round(year_entry['interest'] + amount, 2)
        else:
            yearly_interest.append({'year': year, 'interest': amount})
    
    return yearly_interest