import logging
from datetime import date
from typing import List
from app.models.transaction import Transaction

def categorize_transaction(line, transactions, dividends, interest, transfers, exchange_rates):
    """Categorize transaction based on type."""
    transaction_date = date.fromisoformat(line[0])
    transaction_type = line[1]
    description = line[2]
    amount = round(float(line[3]), 4)
    currency = line[-1]  # Currency was appended as the last element

    if transaction_type == 'DIV':
        symbol = description.split(' ')[0]
        transaction = Transaction(transaction_date, transaction_type, symbol, amount, currency, exchange_rates)
        dividends.append(transaction)
    elif transaction_type == 'FPLINT':
        transaction = Transaction(transaction_date, transaction_type, '', amount, currency, exchange_rates)
        interest.append(transaction)
    elif transaction_type == 'TRFIN' or transaction_type == 'TRFOUT':
        values = description.split(' ')
        if len(values) > 0 and values[0] == 'Money':
            logging.debug("Money transfer, ignoring")
        else:
            # Search for "Transfer of" and get the float value after it
            try:
                shares = None
                for i, value in enumerate(values):
                    if i + 2 < len(values) and value == "Transfer" and values[i + 1] == "of":
                        shares = round(float(values[i + 2]), 4)
                        break
                if shares is None:
                    logging.error("Error: 'Transfer' not found or no value after it")
                    logging.error("Check your algorithm")
                    logging.error(line)
                    exit(1)
            except (ValueError, IndexError):
                logging.error("Error: Could not convert value to float")
                exit(1)
            
            symbol = values[0]
            transaction = Transaction(transaction_date, transaction_type, symbol, amount, currency, exchange_rates, shares)
            transfers.append(transaction)
    else:  # BUY or SELL
        values = description.split(' ')
        # Search for "Bought" or "Sold" and get the float value after it
        try:
            shares = None
            for i, value in enumerate(values):
                if value in ["Bought", "Sold"] and i + 1 < len(values):
                    shares = round(float(values[i + 1]), 4)
                    break
            if shares is None:
                logging.error("Error: 'Bought' or 'Sold' not found or no value after it")
                logging.error("Check your algorithm")
                exit(1)
        except (ValueError, IndexError):
            logging.error("Error: Could not convert value to float")
            exit(1)
        
        symbol = values[0]
        transaction = Transaction(transaction_date, transaction_type, symbol, amount, currency, exchange_rates, shares)
        transactions.append(transaction)

def process_transactions(allTransactions, exchange_rates):
    """Process CSV files and categorize transactions."""
    relevant_transactions = ['BUY', 'SELL', 'DIV', 'FPLINT', 'TRFIN', 'TRFOUT']
    
    transactions = []
    dividends = []
    interest = []
    transfers = []
        
    for transaction in allTransactions:
        if transaction[1] not in relevant_transactions:
            continue
        categorize_transaction(transaction, transactions, dividends, interest, transfers, exchange_rates)
    
    # Sort transactions by date, transaction type, and symbol
    transactions = sorted(transactions, key=lambda t: (t.date, t.transaction_type, t.symbol))    
    return transactions, dividends, interest