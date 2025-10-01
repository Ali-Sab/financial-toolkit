from typing import List
import logging
from app.core.config import USD_TO_CAD_RATES_FILE
from app.utils.exchange_rate import read_usd_to_cad_rates
from app.services.transaction_processor import process_transactions
from app.services.profit_calculator import (
    calculate_yearly_net_profit,
    calculate_yearly_dividends_awarded,
    calculate_yearly_interest_earned
)
from app.services.report_generator import (
    display_net_profit_summary,
    display_dividend_summary,
    display_interest_summary
)

class StockService:
    @staticmethod
    def get_stock_tickers() -> List[str]:
        return ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    
    @staticmethod
    def process_stock_transactions(allTransactions: List[List[str]]) -> dict:
        """Process stock transactions and return complete financial analysis."""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info("Starting program")
        
        exchange_rates = read_usd_to_cad_rates(str(USD_TO_CAD_RATES_FILE))
        logging.info("Read exchange rates")
        
        transactions, dividends, interest = process_transactions(allTransactions, exchange_rates)
        logging.info("Processed CSV files")
        
        logging.info("\n=== Currency: CAD ===")
        net_profit_data, sells = calculate_yearly_net_profit(transactions)
        net_profit_report = display_net_profit_summary(net_profit_data)
        
        dividend_data = calculate_yearly_dividends_awarded(dividends)
        dividend_report = display_dividend_summary(dividend_data)
        
        interest_data = calculate_yearly_interest_earned(interest)
        interest_report = display_interest_summary(interest_data)
        
        logging.info("Read complete")
        
        return {
            "net_profit_data": net_profit_data,
            "dividend_data": dividend_data,
            "interest_data": interest_data,
            "formatted_report": f"{net_profit_report}\n{dividend_report}\n{interest_report}"
        }



