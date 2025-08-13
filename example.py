#!/usr/bin/env python3
"""
💎 Fragment Stars Analyzer - Simple Examples
"""

from fragment_stars import get_stars_rate, stars_to_ton_fragment, ton_to_usdt_binance
import json


def basic_example():
    """Basic usage example"""
    print("💎 Getting Stars → USDT rate...")
    
    result = get_stars_rate()
    
    if result["usdt_per_star"] > 0:
        print(f"✅ 1 Star = ${result['usdt_per_star']:.6f} USDT")
        print(f"✅ 1000 Stars = ${result['usdt_per_star'] * 1000:.2f} USDT")
    else:
        print("❌ Could not get rate")
        for error in result.get("errors", []):
            print(f"  • {error}")


def detailed_example():
    """Detailed example with raw data"""
    print("\n💎 Detailed analysis...")
    
    result = get_stars_rate(limit=30, include_raw=True)
    
    print(f"Fragment transactions: {result.get('fragment_raw', {}).get('transactions_count', 0)}")
    print(f"TON/USDT rate: ${result.get('usdt_per_ton', 0):.3f}")
    
    if result.get("errors"):
        print("Errors:")
        for error in result["errors"]:
            print(f"  • {error}")


def components_example():
    """Example using individual components"""
    print("\n💎 Using components separately...")
    
    try:
        # Get Stars → TON rate
        fragment_data = stars_to_ton_fragment(limit=20)
        print(f"Stars→TON: {fragment_data['ton_per_star']:.6f} TON/Star")
        print(f"Transactions: {fragment_data['transactions_count']}")
        
        # Get TON → USDT rate
        binance_data = ton_to_usdt_binance()
        if binance_data:
            print(f"TON→USDT: ${binance_data['usdt_per_ton']:.3f}")
        
    except Exception as e:
        print(f"Error: {e}")


def json_example():
    """JSON output example"""
    print("\n💎 JSON output...")
    
    result = get_stars_rate(limit=10)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    print("🚀 Fragment Stars Analyzer Examples")
    print("=" * 40)
    
    basic_example()
    detailed_example()
    components_example()
    json_example()
    
    print("\n✅ Done!")