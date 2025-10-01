def display_net_profit_summary(net_profit_summary):
    """Display net profit summary by stock/year and year totals."""
    output = []
    
    # Group by stock
    stocks = {}
    for entry in net_profit_summary:
        stock = entry['stock']
        if stock not in stocks:
            stocks[stock] = []
        stocks[stock].append({'year': entry['year'], 'net_profit': entry['net_profit']})

    # Display by stock
    output.append("\nNet Profit by Stock:")
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
    
    report = "\n".join(output)
    print(report)
    return report

def display_dividend_summary(yearly_dividends):
    """Display dividend summary by stock/year and year totals."""
    output = []
    
    # Group by stock
    stocks = {}
    for entry in yearly_dividends:
        stock = entry['stock']
        if stock not in stocks:
            stocks[stock] = []
        stocks[stock].append({'year': entry['year'], 'dividends': entry['dividends']})
    
    # Display by stock
    output.append("\nDividends by Stock:")
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
    
    report = "\n".join(output)
    print(report)
    return report

def display_interest_summary(yearly_interest):
    """Display interest summary by year."""
    output = []
    output.append("\nInterest by Year:")
    for entry in sorted(yearly_interest, key=lambda x: x['year']):
        output.append(f"  {entry['year']}: ${entry['interest']}")
    
    report = "\n".join(output)
    print(report)
    return report