from typing import List
import logging
from app.core.config import USD_TO_CAD_RATES_FILE
from app.utils.exchange_rate import read_usd_to_cad_rates
from app.services.transaction_processor import process_transactions
from app.services.profit_calculator import FinancialCalculator
from app.services.report_generator import ReportGenerator

class StockService:
    @staticmethod
    def get_stock_tickers() -> List[str]:
        return ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    
    @staticmethod
    def log_cls_transactions(transactions: List) -> None:
        """Log all transactions with symbol 'CLS'."""
        for transaction in transactions:
            if hasattr(transaction, 'symbol') and transaction.symbol == 'CLS':
                logging.info(f"CLS Transaction: {transaction}")
    
    @staticmethod
    def process_stock_transactions(allTransactions: List[List[str]]) -> dict:
        """Process stock transactions and return complete financial analysis."""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info("Starting program")
        
        # Load exchange rates and process transactions
        exchange_rates = read_usd_to_cad_rates(str(USD_TO_CAD_RATES_FILE))
        logging.info("Read exchange rates")
        
        transactions, dividends, interest = process_transactions(allTransactions, exchange_rates)
        logging.info("Processed CSV files")
        
        # Log CLS transactions
        StockService.log_cls_transactions(transactions)
        
        # Calculate all financial data
        logging.info("\n=== Currency: CAD ===")
        financial_data = FinancialCalculator.calculate_all_financial_data(transactions, dividends, interest)
        
        # Generate complete report
        formatted_report = ReportGenerator.generate_complete_report(
            financial_data['net_profit_data'],
            financial_data['dividend_data'],
            financial_data['interest_data']
        )
        
        logging.info("Read complete")
        
        return {
            "net_profit_data": financial_data['net_profit_data'],
            "dividend_data": financial_data['dividend_data'],
            "interest_data": financial_data['interest_data'],
            "sells": financial_data['sells'],
            "formatted_report": formatted_report
        }



