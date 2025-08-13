# Telegram Stars ↔ USDT Converter

Real-time Telegram Stars to USDT exchange rate converter using Fragment blockchain data.

## Features

- 🔄 Real-time Stars ↔ USDT conversion
- 📊 Exchange rate statistics (min/max/median)
- 📱 Mobile-responsive design
- ⚡ Updated daily via GitHub Actions
- 🔗 Direct Fragment blockchain integration

## Data Source

Exchange rates are calculated from real Fragment transactions:
- **Stars → TON**: Fragment blockchain transactions
- **TON → USDT**: Binance API
- **Update frequency**: Daily at 12:00 UTC

## GitHub Pages Setup

1. Enable GitHub Pages in repository settings
2. Set source to "GitHub Actions"
3. The workflow will automatically:
   - Fetch latest exchange rates
   - Generate `rates.json`
   - Deploy to GitHub Pages

## Local Development

```bash
# Generate rates locally
python scripts/generate_rates.py

# Serve locally
python -m http.server 8000 -d github_pages
```

## API

The site uses a simple JSON API:

```json
{
  "usdt_per_star": 0.012345,
  "ton_per_star": 0.002500,
  "usdt_per_ton": 4.938000,
  "timestamp": "2024-01-01T12:00:00Z",
  "fragment_raw": {
    "transactions_count": 50,
    "min_rate": 0.002400,
    "max_rate": 0.002600,
    "median_rate": 0.002500
  },
  "errors": []
}
```