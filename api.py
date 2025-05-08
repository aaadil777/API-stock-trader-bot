# IH#4 Familiarity – same naming as many public REST wrappers
# IH#8 Protection     – error handling prevents hard crashes

import os, random, requests
from dotenv import load_dotenv

load_dotenv()                       # look for .env file
API_KEY = os.getenv("AV_KEY")       # Alpha Vantage key (do NOT commit)

class StockAPI:
    BASE = "https://www.alphavantage.co/query"

    @staticmethod
    def get_quote(symbol: str) -> float | None:
        """
        Return *latest* price for `symbol`.
        Falls back to a random price so the demo never stalls.
        """
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY or "demo",
        }
        try:
            r = requests.get(StockAPI.BASE, params=params, timeout=5)
            r.raise_for_status()
            data = r.json().get("Global Quote", {})
            price = float(data.get("05. price", "nan"))
            return price if price == price else None
        except Exception:
            # IH#8 Protection – graceful fallback
            return round(random.uniform(10, 500), 2)