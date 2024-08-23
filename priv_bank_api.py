import aiohttp
import ssl
from typing import Dict, List

class PrivatBankAPI:
    API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def get_exchange_rates(self, date: str, currencies: List[str]) -> Dict[str, Dict[str, float]]:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.API_URL + date, ssl=ssl_context) as response:
                    if response.status == 200:
                        data = await response.json()
                        rates = data.get("exchangeRate", [])
                        return {currency: self._extract_currency_rate(currency, rates) for currency in currencies}
                    else:
                        print(f"Error fetching data for {date}: HTTP {response.status}")
                        return {}
            except aiohttp.ClientError as e:
                print(f"Network error: {e}")
                return {}

    def _extract_currency_rate(self, currency: str, rates: List[Dict]) -> Dict[str, float]:
        for rate in rates:
            if rate.get("currency") == currency:
                return {"sale": rate.get("saleRate"), "purchase": rate.get("purchaseRate")}
        return {"sale": None, "purchase": None}
