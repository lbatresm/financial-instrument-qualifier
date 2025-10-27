import json
from pathlib import Path
import pandas as pd


def _load_fund_data(json_file_path: Path) -> dict:
    """
    Loads fund data from a JSON file.
    
    Args:
        json_file_path: Path to the JSON file
        
    Returns:
        dict: Dictionary with fund data
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        fund_dict = json.load(f)
    return fund_dict


def _save_fund_data(json_file_path: Path, fund_dict: dict) -> None:
    """
    Saves fund data to a JSON file.
    
    Args:
        json_file_path: Path to the JSON file
        fund_dict: Dictionary with fund data
    """
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(fund_dict, f, indent=2, ensure_ascii=False)


def _compute_SSRI(fund_dict: dict) -> dict:
    """
    SRRI (Synthetic Risk and Reward Indicator). Computed with 5 years volatility
    
    Args:
        fund_dict: Dictionary with fund data
        
    Returns:
        dict: Modified dictionary with SSRI added before 'fee'
    """
    # Get 5-year volatility (M60 = 60 months)
    M60_vol = fund_dict.get('volatility', {}).get('M60', 0)

    # Compute SSRI based on volatility ranges
    if M60_vol < 0.50:
        SSRI = 1
    elif M60_vol < 2.00:
        SSRI = 2
    elif M60_vol < 5.00:
        SSRI = 3
    elif M60_vol < 10.00:
        SSRI = 4
    elif M60_vol < 15.00:
        SSRI = 5
    elif M60_vol < 25.00:
        SSRI = 6
    else:  # >= 25.00
        SSRI = 7

    # Create new dictionary with SSRI inserted before 'fee'
    new_dict = {}
    for k, v in fund_dict.items():
        if k == 'fee':
            # Insert SSRI key-value pair just before 'fee'
            new_dict['SSRI'] = SSRI
        new_dict[k] = v

    return new_dict



def main():
    fund_json_path = Path(__file__).parent.parent / "finect" / "fund_ES0179172038.json"
    
    # Load fund data
    fund_dict = _load_fund_data(fund_json_path)
    
    # Compute and insert SSRI
    fund_dict = _compute_SSRI(fund_dict)
    
    # Save updated data back to JSON file
    _save_fund_data(fund_json_path, fund_dict)
    

if __name__ == "__main__":
    main()



