class ReportGenerator:
    @staticmethod
    def generate_net_profit_report(net_profit_summary):
        """Generate net profit summary report."""
        output = []
        
        # Group by stock
        stocks = {}
        for entry in net_profit_summary:
            stock = entry['stock']
            if stock not in stocks:
                stocks[stock] = []
            stocks[stock].append({'year': entry['year'], 'net_profit': entry['net_profit']})

        # Display by stock
        output.append("Net Profit by Stock:")
        for stock, years in sorted(stocks.items()):
            output.append(f"  {stock}:")
            for year_data in sorted(years, key=lambda x: x['year']):
                output.append(f"    {year_data['year']}: ${year_data['net_profit']:.2f}")

        # Group by year
        years = {}
        for entry in net_profit_summary:
            year = entry['year']
            if year not in years:
                years[year] = {'total': 0, 'stocks': []}
            years[year]['total'] += entry['net_profit']
            years[year]['stocks'].append({'stock': entry['stock'], 'net_profit': entry['net_profit']})

        # Display by year
        output.append("\nNet Profit by Year:")
        for year in sorted(years.keys()):
            output.append(f"  {year}: ${round(years[year]['total'], 2)} total")
            for stock_data in years[year]['stocks']:
                output.append(f"    {stock_data['stock']}: ${stock_data['net_profit']}")
        
        return "\n".join(output)

    @staticmethod
    def generate_dividend_report(yearly_dividends):
        """Generate dividend summary report."""
        output = []
        
        # Group by stock
        stocks = {}
        for entry in yearly_dividends:
            stock = entry['stock']
            if stock not in stocks:
                stocks[stock] = []
            stocks[stock].append({'year': entry['year'], 'dividends': entry['dividends']})
        
        # Display by stock
        output.append("Dividends by Stock:")
        for stock, years in stocks.items():
            output.append(f"  {stock}:")
            for year_data in sorted(years, key=lambda x: x['year']):
                output.append(f"    {year_data['year']}: ${year_data['dividends']}")
        
        # Group by year
        years = {}
        for entry in yearly_dividends:
            year = entry['year']
            if year not in years:
                years[year] = {'total': 0, 'stocks': []}
            years[year]['total'] += entry['dividends']
            years[year]['stocks'].append({'stock': entry['stock'], 'dividends': entry['dividends']})
        
        # Display by year
        output.append("\nDividends by Year:")
        for year in sorted(years.keys()):
            output.append(f"  {year}: ${round(years[year]['total'], 2)} total")
            for stock_data in years[year]['stocks']:
                output.append(f"    {stock_data['stock']}: ${stock_data['dividends']}")
        
        return "\n".join(output)

    @staticmethod
    def generate_interest_report(yearly_interest):
        """Generate interest summary report."""
        output = []
        output.append("Interest by Year:")
        for entry in sorted(yearly_interest, key=lambda x: x['year']):
            output.append(f"  {entry['year']}: ${entry['interest']}")
        
        return "\n".join(output)
    
    @classmethod
    def generate_complete_report(cls, net_profit_data, dividend_data, interest_data):
        """Generate complete financial report."""
        reports = [
            cls.generate_net_profit_report(net_profit_data),
            cls.generate_dividend_report(dividend_data),
            cls.generate_interest_report(interest_data)
        ]
        return "\n\n".join(reports)