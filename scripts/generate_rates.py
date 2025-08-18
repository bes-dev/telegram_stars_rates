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
        
        # Update historical data
        history_file = github_pages_dir / 'history.json'
        history_data = []
        
        # Load existing history
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                    # Validate existing data structure
                    if not isinstance(history_data, list):
                        history_data = []
            except Exception as e:
                print(f"⚠️ Could not load existing history: {e}")
                history_data = []
        
        # Add current data point (only if we have valid rates)
        if rates_data["usdt_per_star"] > 0:
            current_point = {
                "date": rates_data["timestamp"][:10],  # YYYY-MM-DD format
                "timestamp": rates_data["timestamp"],
                "usdt_per_star": round(rates_data["usdt_per_star"], 6),
                "ton_per_star": round(rates_data["ton_per_star"], 6),
                "usdt_per_ton": round(rates_data["usdt_per_ton"], 3)
            }
            
            today = current_point["date"]
            
            # Check if we already have an entry for today
            existing_today = None
            for i, h in enumerate(history_data):
                if h.get("date") == today:
                    existing_today = i
                    break
            
            if existing_today is not None:
                # Update existing entry for today (better rate data)
                history_data[existing_today] = current_point
                print(f"📊 Updated existing entry for {today}")
            else:
                # Add new entry for new day
                history_data.append(current_point)
                print(f"➕ Added new entry for {today}")
            
            # Sort by date and keep only last 90 days
            history_data = sorted(history_data, key=lambda x: x["date"])
            if len(history_data) > 90:
                removed_count = len(history_data) - 90
                history_data = history_data[-90:]
                print(f"🗑️ Removed {removed_count} old entries, keeping last 90 days")
        
        # Save updated history
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated {rates_file}")
        print(f"✅ Generated {api_file}")
        print(f"✅ Updated {history_file} ({len(history_data)} data points)")
        print(f"💰 Current rate: 1 Star = ${rates_data['usdt_per_star']:.6f} USDT")
        
        if rates_data.get('errors'):
            print("⚠️ Warnings:", rates_data['errors'])
            
    except Exception as e:
        print(f"❌ Error generating rates: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()