from scraper.nse_session import get_nse_session
from config.config import NSE_BASE_URL, OPTION_CHAIN_API, REQUEST_TIMEOUT

def fetch_option_chain(symbol: str) -> dict:
    session = get_nse_session()
    url = NSE_BASE_URL + OPTION_CHAIN_API + symbol.upper()
    response = session.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()
