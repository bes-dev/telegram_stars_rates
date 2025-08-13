#!/usr/bin/env python3
"""
Generate rates.json for GitHub Pages
"""

import json
import sys
import os
from pathlib import Path

# Add telegram_stars_rates to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from telegram_stars_rates.analyzer import get_stars_rate

def main():
    """Generate rates.json file for GitHub Pages."""
    try:
        # Get exchange rates with raw data
        rates_data = get_stars_rate(
            limit=100,  # More transactions for better accuracy
            include_raw=True
        )
        
        if rates_data.get('usdt_per_star', 0) <= 0:
            print("ERROR: Invalid exchange rate data")
            print("Errors:", rates_data.get('errors', []))
            sys.exit(1)
        
        # Ensure github_pages directory exists
        github_pages_dir = Path(__file__).parent.parent / 'github_pages'
        github_pages_dir.mkdir(exist_ok=True)
        
        # Write rates.json
        rates_file = github_pages_dir / 'rates.json'
        with open(rates_file, 'w', encoding='utf-8') as f:
            json.dump(rates_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated {rates_file}")
        print(f"💰 Current rate: 1 Star = ${rates_data['usdt_per_star']:.6f} USDT")
        
        if rates_data.get('errors'):
            print("⚠️ Warnings:", rates_data['errors'])
            
    except Exception as e:
        print(f"❌ Error generating rates: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()