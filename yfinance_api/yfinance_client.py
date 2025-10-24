import yfinance as yf
import pandas as pd

def get_fund_info(symbol: str) -> dict:
    """
    https://ranaroussi.github.io/yfinance/reference/api/yfinance.Ticker.funds_data.html
    """
    try:
        # Create Ticker object
        ticker = yf.Ticker(symbol)
        
        # Obtain ETF or index fund information using funds_data
        fund_data = ticker.funds_data
        
        fund_info = {
            'symbol': symbol,
            'asset_classes': fund_data.asset_classes,
            'bond_holdings': fund_data.bond_holdings,
            'bond_ratings': fund_data.bond_ratings,
            'description': fund_data.description,
            'equity_holdings': fund_data.equity_holdings,
            'fund_operations': fund_data.fund_operations,
            'fund_overview': fund_data.fund_overview,
            'sector_weightings': fund_data.sector_weightings,
            'top_holdings': fund_data.top_holdings
        }
        
        return fund_info
        
    except Exception as e:
        print(f"Error obtaining fund info for {symbol}: {e}")
        return None

def main():
    # Example usage
    fund_symbol = "0P0001CLDK.F" 
    
    print(f"Getting fund information for {fund_symbol}...")
    fund_info = get_fund_info(fund_symbol)
    
    if fund_info:
        print(f"\n=== FUND OVERVIEW ===")
        print(fund_info['fund_overview'])
        
        print(f"\n=== DESCRIPTION ===")
        print(fund_info['description'])
        
        print(f"\n=== ASSET CLASSES ===")
        print(fund_info['asset_classes'])
        
        print(f"\n=== TOP HOLDINGS ===")
        print(fund_info['top_holdings'])
        
        print(f"\n=== EQUITY HOLDINGS ===")
        print(fund_info['equity_holdings'])
        
        print(f"\n=== BOND HOLDINGS ===")
        print(fund_info['bond_holdings'])
        
        print(f"\n=== BOND RATINGS ===")
        print(fund_info['bond_ratings'])
        
        print(f"\n=== SECTOR WEIGHTINGS ===")
        print(fund_info['sector_weightings'])
        
        print(f"\n=== FUND OPERATIONS ===")
        print(fund_info['fund_operations'])
    else:
        print("Could not obtain fund information")

if __name__ == "__main__":
    main()