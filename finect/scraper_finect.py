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
        
        # Save HTML for debugging (overwrite if exists)
        debug_html_file = f"finect/debug_html_{isin}.html" if isin else "finect/debug_html.html"
        try:
            with open(debug_html_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"HTML saved to {debug_html_file}")
        except Exception as e:
            print(f"Warning: Could not save HTML: {e}")
        
        # Extract INITIAL_STATE
        match = re.search(r'window.INITIAL_STATE="([^"]+)"', response.text)
        if not match:
            print("INITIAL_STATE not found in the page")
            return None
        
        # Decode URL encoded data
        decoded = unquote(match.group(1))
        data = json.loads(decoded)
        
        # Save INITIAL_STATE JSON for debugging (overwrite if exists)
        initial_state_file = f"finect/initial_state_{isin}.json" if isin else "finect/initial_state.json"
        try:
            with open(initial_state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"INITIAL_STATE saved to {initial_state_file}")
        except Exception as e:
            print(f"Warning: Could not save INITIAL_STATE: {e}")
        
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
    
    # Extract category (just name, not description)
    category_name = fund_model.get('category', {}).get('name', 'N/A')
    
    # Extract strategy statement
    strategy = fund_model.get('strategy', {})
    
    # Extract Morningstar rating
    ratings = fund_model.get('ratings', [])
    morningstar_rating = None
    for rating in ratings:
        if rating.get('provider') == 'morningstar':
            morningstar_rating = rating.get('value')
            break

    # Extract benchmark
    benchmarks = fund_model.get('benchmarks', [])
    benchmark_name = ""
    if benchmarks and len(benchmarks) > 0:
        benchmark_name = benchmarks[0].get('name', '')

    # Extract availability in platforms
    comparers = fund_model.get('comparer', [])
    platform_names = []
    if comparers and len(comparers) > 0:
        for comparer in comparers:
            platform_name = comparer.get('name', '')
            if platform_name:
                platform_names.append(platform_name)

    # Extract currency
    currency = fund_model.get('currency', {}).get('code', {})

    # Extract number of classes of the fund
    classes = fund_model.get('classes', [])  
    num_classes = len(classes) if classes else 0

    # Extract fees/commissions from classes
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
    
    # Extract max drawdown
    max_drawdown = fund_stats.get('maxDrawdown', [])
    drawdown_by_period = {}
    for dd in max_drawdown:
        period = dd.get('period', '')
        value = dd.get('value')
        if value is not None:
            drawdown_by_period[period] = value

    # Extract volatility (standard deviation)
    standard_deviation = fund_stats.get('standardDeviation', [])
    volatility_by_period = {}
    for vol in standard_deviation:
        period = vol.get('period', '')
        value = vol.get('value')
        if value is not None:
            volatility_by_period[period] = value
    
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
    
    # Extract tracking error
    tracking_error = fund_stats.get('trackingError', [])
    tracking_error_by_period = {}
    for te in tracking_error:
        period = te.get('period', '')
        value = te.get('value')
        if value is not None:
            tracking_error_by_period[period] = value
    
    # Extract correlation
    correlation = fund_stats.get('correlation', [])
    correlation_by_period = {}
    for corr in correlation:
        period = corr.get('period', '')
        value = corr.get('value')
        if value is not None:
            correlation_by_period[period] = value
    
    # Extract R-squared (r2)
    r2 = fund_stats.get('r2', [])
    r2_by_period = {}
    for r in r2:
        period = r.get('period', '')
        value = r.get('value')
        if value is not None:
            r2_by_period[period] = value

    # Extract returns/performance (annualized only)
    performance = fund_stats.get('performance', {})
    returns_by_period = {}
    if performance and performance.get('periods'):
        for ret in performance['periods']:
            # Filter only annualized returns, not accumulated
            if ret.get('type') == 'annualized':
                period = ret.get('period', '')
                value = ret.get('value')
                if value is not None:
                    returns_by_period[period] = value
    
    # Extract current value
    current_value = ""
    if classes and len(classes) > 0:
        last_quote = classes[0].get('lastQuote', {})
        if last_quote and last_quote.get('price'):
            current_value = f"{last_quote['price']:.2f}€"
    
    # Extract breakdown data (asset allocation, market cap, regional exposure, stock sector)
    breakdown_data = {}
    breakdown = fund_model.get('breakdown', [])
    if breakdown:
        for b in breakdown:
            breakdown_type = b.get('type')
            items = b.get('items', [])
            breakdown_data[breakdown_type] = []
            for item in items:
                drawer = item.get('drawer', '')
                values = item.get('values', {})
                long_val = values.get('long', 0)
                if long_val > 0:  # Only include items with positive allocation
                    breakdown_data[breakdown_type].append({
                        'name': drawer,
                        'value': long_val
                    })

    # Extract portfolio holdings (name and weight)
    portfolio = fund_model.get('portfolio', {})
    holdings_data = []
    if portfolio and portfolio.get('holdings'):
        for holding in portfolio['holdings']:
            holding_name = holding.get('name', '')
            holding_weight = holding.get('weight', 0)
            if holding_name:
                holdings_data.append({
                    'name': holding_name,
                    'weight': holding_weight
                })

    # Build fund data
    fund_data = {
        'isin': isin,
        'name': fund_model.get('name', 'N/A'),
        'fund_manager': mgmt_company.get('name', 'N/A'),
        'category': category_name,
        'benchmark': benchmark_name,
        'value': current_value,
        'description': fund_model.get('description', ''),
        'strategy': strategy if isinstance(strategy, str) else 'N/A',
        'morningstar_rating': morningstar_rating,
        'num_classes': num_classes,
        'fee': fee_data,
        'returns': returns_by_period,
        'volatility': volatility_by_period,
        'max_drawdown': drawdown_by_period,
        'alpha': alpha_by_period,
        'beta': beta_by_period,
        'sharpe': sharpe_by_period,
        'tracking_error': tracking_error_by_period,
        'correlation': correlation_by_period,
        'r2': r2_by_period,
        'breakdown': breakdown_data,
        'holdings': holdings_data,
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
        
        morningstar = fund_data.get('morningstar_rating')
        if morningstar is not None:
            print(f"Morningstar Rating: {morningstar}/5")
        
        num_classes = fund_data.get('num_classes')
        if num_classes is not None:
            print(f"Number of Classes: {num_classes}")
        
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
        
        print("\nTracking Error by Period:")
        for period, value in fund_data.get('tracking_error', {}).items():
            if value is not None:
                print(f"  {period}: {value:.2f}")
        
        print("\nCorrelation by Period:")
        for period, value in fund_data.get('correlation', {}).items():
            if value is not None:
                print(f"  {period}: {value:.2f}%")
        
        print("\nR-squared by Period:")
        for period, value in fund_data.get('r2', {}).items():
            if value is not None:
                print(f"  {period}: {value:.2f}%")
        
        # Print breakdown data
        breakdown = fund_data.get('breakdown', {})
        if breakdown:
            print("\nBreakdown:")
            for breakdown_type, items in breakdown.items():
                print(f"  {breakdown_type.replace('-', ' ').title()}:")
                for item in items[:5]:  # Show top 5 items
                    print(f"    {item['name']}: {item['value']:.2f}%")
        
        # Print holdings
        holdings = fund_data.get('holdings', [])
        if holdings:
            print(f"\nTop Holdings ({len(holdings)} total):")
            for holding in holdings[:10]:  # Show top 10 holdings
                if isinstance(holding, dict):
                    print(f"  - {holding.get('name', 'N/A')}: {holding.get('weight', 0):.2f}%")
                else:
                    print(f"  - {holding}")
        
        # Save to JSON
        save_to_json(fund_data, f'finect/fund_{isin}.json')
        
    else:
        print("Failed to retrieve fund information")


if __name__ == "__main__":
    main()
