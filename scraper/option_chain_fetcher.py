# scraper/option_chain_fetcher.py
import time
from scraper.nse_session import nse_session

def fetch_option_chain(symbol: str):
    symbol = symbol.upper()

    if symbol in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"]:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    else:
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"

    for attempt in range(3):
        resp = nse_session.get(url)

        if resp.status_code == 200:
            data = resp.json()
            if "records" in data:
                return data

        time.sleep(1)

    raise Exception("NSE blocked or returned invalid data")
