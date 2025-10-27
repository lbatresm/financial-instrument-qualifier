"""
Web Scraper for Finect - Investment Fund
Extracts data from the page's React initial state (INITIAL_STATE)

IMPORTANT WARNING:
- This script is for educational and research purposes only
- YOU MUST verify and respect Finect's terms of service
- Do not use this script for commercial purposes without authorization
- Implement delays between requests to avoid overloading the server
- Consider using official APIs if available

Source: https://www.finect.com/fondos-inversion/
"""

import requests
import json
import re
from urllib.parse import unquote
from typing import Dict, Optional


def scrape_fund_info(url: str, isin: str = "") -> Optional[Dict]:
    """
    Scrapes fund information from Finect website by extracting INITIAL_STATE
    
    Args:
        url: Full URL of the fund page
        isin: Optional ISIN code
    
    Returns:
        Dictionary with fund information or None if error
    """
    
    try:
        # Headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        }
        
        print(f"Fetching data from: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Extract INITIAL_STATE
        match = re.search(r'window.INITIAL_STATE="([^"]+)"', response.text)
        if not match:
            print("INITIAL_STATE not found in the page")
            return None
        
        # Decode URL encoded data
        decoded = unquote(match.group(1))
        data = json.loads(decoded)
        
        # Extract fund information
        fund_data = extract_fund_data(data, isin)
        
        return fund_data
        
    except Exception as e:
        print(f"Error fetching/parsing data: {e}")
        return None


def extract_fund_data(data: Dict, isin: str = "") -> Dict:
    """Extract fund data from INITIAL_STATE"""
    
    # Navigate to fund data
    fund_model = data.get('fund', {}).get('fund', {}).get('model', {})
    fund_stats = fund_model.get('stats', {})
    fund_metrics = data.get('fund', {}).get('fund', {}).get('metrics', {})
    
    # Extract ISIN if not provided
    if not isin:
        isin = fund_model.get('isin', '')
    
    # Extract management company
    mgmt_company = fund_model.get('managementCompany', {})
    
    # Extract category
    category = fund_model.get('category', {})
    
    # Extract fees/commissions from classes
    classes = fund_model.get('classes', [])
    fee_data = {}
    if classes and len(classes) > 0:
        fees_obj = classes[0].get('fees', {})
        
        # Extract each fee type (fees is an object with keys like 'mgr', 'red', etc.)
        if fees_obj.get('mgr'):
            fee_data['management'] = fees_obj['mgr'].get('value', 0)
        if fees_obj.get('red'):
            fee_data['redemption'] = fees_obj['red'].get('value', 0)
        if fees_obj.get('cus'):
            fee_data['custody'] = fees_obj['cus'].get('value', 0)
        if fees_obj.get('flo'):
            fee_data['subscription'] = fees_obj['flo'].get('value', 0)
        if fees_obj.get('ter'):
            fee_data['expense_ratio'] = fees_obj['ter'].get('value', 0)
        if fees_obj.get('ogc'):
            fee_data['ongoing_charge'] = fees_obj['ogc'].get('value', 0)
    
    # Extract returns/performance
    performance = fund_stats.get('performance', {})
    returns_by_period = {}
    if performance and performance.get('periods'):
        for ret in performance['periods']:
            period = ret.get('period', '')
            value = ret.get('value')
            if value is not None:
                returns_by_period[period] = value
    
    # Extract volatility (standard deviation)
    standard_deviation = fund_stats.get('standardDeviation', [])
    volatility_by_period = {}
    for vol in standard_deviation:
        period = vol.get('period', '')
        value = vol.get('value')
        if value is not None:
            volatility_by_period[period] = value
    
    # Extract max drawdown
    max_drawdown = fund_stats.get('maxDrawdown', [])
    drawdown_by_period = {}
    for dd in max_drawdown:
        period = dd.get('period', '')
        value = dd.get('value')
        if value is not None:
            drawdown_by_period[period] = value
    
    # Extract alpha
    alpha = fund_stats.get('alpha', [])
    alpha_by_period = {}
    for a in alpha:
        period = a.get('period', '')
        value = a.get('value')
        if value is not None:
            alpha_by_period[period] = value
    
    # Extract beta
    beta = fund_stats.get('beta', [])
    beta_by_period = {}
    for b in beta:
        period = b.get('period', '')
        value = b.get('value')
        if value is not None:
            beta_by_period[period] = value
    
    # Extract sharpe ratio
    sharpe = fund_stats.get('sharpeRatio', [])
    sharpe_by_period = {}
    for s in sharpe:
        period = s.get('period', '')
        value = s.get('value')
        if value is not None:
            sharpe_by_period[period] = value
    
    # Extract benchmark
    benchmarks = fund_model.get('benchmarks', [])
    benchmark_name = ""
    if benchmarks and len(benchmarks) > 0:
        benchmark_name = benchmarks[0].get('name', '')
    
    # Extract current value
    current_value = ""
    if classes and len(classes) > 0:
        last_quote = classes[0].get('lastQuote', {})
        if last_quote and last_quote.get('price'):
            current_value = f"{last_quote['price']:.2f}€"
    
    # Build fund data
    fund_data = {
        'isin': isin,
        'name': fund_model.get('name', 'N/A'),
        'fund_manager': mgmt_company.get('name', 'N/A'),
        'category': category.get('name', 'N/A'),
        'benchmark': benchmark_name,
        'value': current_value,
        'description': fund_model.get('description', ''),
        'fee': fee_data,
        'returns': returns_by_period,
        'volatility': volatility_by_period,
        'max_drawdown': drawdown_by_period,
        'alpha': alpha_by_period,
        'beta': beta_by_period,
        'sharpe': sharpe_by_period,
    }
    
    return fund_data


def save_to_json(data: Dict, filename: str = 'fund_data.json'):
    """Save fund data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")


def main():
    """Example usage"""
    
    url = "https://www.finect.com/fondos-inversion/ES0179172038-Liberty_euro_stock_market_fi"
    isin = "ES0179172038"
    
    print("=" * 50)
    print("Finect Web Scraper - Extracting from INITIAL_STATE")
    print("=" * 50)
    
    # Scrape fund information
    fund_data = scrape_fund_info(url, isin)
    
    if fund_data:
        print("\nFund Information Retrieved:")
        print("-" * 50)
        
        print(f"Name: {fund_data.get('name', 'N/A')}")
        print(f"Fund Manager: {fund_data.get('fund_manager', 'N/A')}")
        print(f"Category: {fund_data.get('category', 'N/A')}")
        print(f"Benchmark: {fund_data.get('benchmark', 'N/A')}")
        print(f"Current Value: {fund_data.get('value', 'N/A')}")
        
        print("\nFees:")
        fees = fund_data.get('fee', {})
        for key, value in fees.items():
            if value is not None and value != 0:
                print(f"  {key}: {value}%")
        
        print("\nReturns by Period:")
        for period, value in fund_data.get('returns', {}).items():
            if value is not None:
                print(f"  {period}: {value:.2f}%")
        
        print("\nVolatility by Period:")
        for period, value in fund_data.get('volatility', {}).items():
            if value is not None:
                print(f"  {period}: {value:.2f}%")
        
        print("\nSharpe Ratio by Period:")
        for period, value in fund_data.get('sharpe', {}).items():
            if value is not None:
                print(f"  {period}: {value:.4f}")
        
        print("\nBeta by Period:")
        for period, value in fund_data.get('beta', {}).items():
            if value is not None:
                print(f"  {period}: {value:.4f}")
        
        print("\nAlpha by Period:")
        for period, value in fund_data.get('alpha', {}).items():
            if value is not None:
                print(f"  {period}: {value:.4f}")
        
        # Save to JSON
        save_to_json(fund_data, f'fund_{isin}.json')
        
    else:
        print("Failed to retrieve fund information")


if __name__ == "__main__":
    main()
