import csv
import logging
from datetime import timedelta
from app.models.exchange_rate import ExchangeRate

def get_exchange_rate(exchange_rates, target_date):
    """Given a target date, identify the most recently defined exchange rate"""
    first_date = next(iter(exchange_rates))
    while target_date >= first_date:
        if target_date in exchange_rates:
            return exchange_rates[target_date].rate
        target_date = target_date - timedelta(days=1)
    
    logging.error("Couldn't find a valid exchange rate for date")
    exit(1)

def read_usd_to_cad_rates(filename):
    """Read USD to CAD exchange rates from a CSV file."""
    from datetime import date
    exchange_rates = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rate_date = date.fromisoformat(row['Date'])
            exchange_rates[rate_date] = ExchangeRate(rate_date, float(row['FXUSDCAD']))
    return exchange_rates