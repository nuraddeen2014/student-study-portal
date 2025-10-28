Exchange Rate API setup

This project uses ExchangeRate-API (https://www.exchangerate-api.com/) for currency conversion.

Steps to enable currency conversion:

1. Install the `requests` package if not already installed:

   pip install requests

2. Obtain a free API key from https://www.exchangerate-api.com/ and set it in your Django settings. Edit `studentstudyportal/settings.py` and set:

   EXCHANGE_RATE_API_KEY = 'your_api_key_here'

   For production, prefer loading the key from environment variables.

3. Restart the Django development server.

Notes:
- The conversion form uses ISO currency codes (USD, EUR, GBP, JPY, NGN, etc.).
- If the API key is missing or network calls fail, the UI will display a helpful error message instead of crashing.
