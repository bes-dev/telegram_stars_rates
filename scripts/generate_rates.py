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
        print("🔍 Starting rate generation...")
        print(f"📁 Current working directory: {os.getcwd()}")
        print(f"📄 Script path: {Path(__file__).parent.parent}")
        
        # Get exchange rates with raw data
        print("🌐 Calling get_stars_rate API...")
        rates_data = get_stars_rate(
            limit=100,  # More transactions for better accuracy
            include_raw=True
        )
        
        print(f"📊 Raw response received: {type(rates_data)}")
        print(f"🔑 Response keys: {list(rates_data.keys()) if isinstance(rates_data, dict) else 'Not a dict'}")
        
        # Debug detailed response
        print(f"💰 ton_per_star: {rates_data.get('ton_per_star', 'N/A')}")
        print(f"💵 usdt_per_ton: {rates_data.get('usdt_per_ton', 'N/A')}")  
        print(f"⭐ usdt_per_star: {rates_data.get('usdt_per_star', 'N/A')}")
        print(f"❌ errors: {rates_data.get('errors', 'N/A')}")
        
        if 'binance_raw' in rates_data:
            print(f"🏦 binance_raw: {rates_data['binance_raw']}")
        
        if rates_data.get('usdt_per_star', 0) <= 0:
            print("ERROR: Invalid exchange rate data")
            print("Errors:", rates_data.get('errors', []))
            sys.exit(1)
        
        # Ensure github_pages directory exists
        github_pages_dir = Path(__file__).parent.parent / 'github_pages'
        github_pages_dir.mkdir(exist_ok=True)
        
        # Write rates.json (full data)
        rates_file = github_pages_dir / 'rates.json'
        with open(rates_file, 'w', encoding='utf-8') as f:
            json.dump(rates_data, f, indent=2, ensure_ascii=False)
        
        # Write api.json (simplified for API consumers)
        api_data = {
            "usdt_per_star": rates_data["usdt_per_star"],
            "ton_per_star": rates_data["ton_per_star"], 
            "usdt_per_ton": rates_data["usdt_per_ton"],
            "timestamp": rates_data["timestamp"],
            "transactions_analyzed": rates_data.get("fragment_raw", {}).get("transactions_count", 0),
            "source": "fragment_blockchain_analysis",
            "rate_source": rates_data.get("binance_raw", {}).get("source", "unknown"),
            "last_updated": rates_data["timestamp"]
        }
        
        api_file = github_pages_dir / 'api.json'
        with open(api_file, 'w', encoding='utf-8') as f:
            json.dump(api_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated {rates_file}")
        print(f"✅ Generated {api_file}")
        print(f"💰 Current rate: 1 Star = ${rates_data['usdt_per_star']:.6f} USDT")
        
        if rates_data.get('errors'):
            print("⚠️ Warnings:", rates_data['errors'])
            
    except Exception as e:
        print(f"❌ Error generating rates: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()