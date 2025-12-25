import requests
from config.config import NSE_BASE_URL, HEADERS

_session = None

def get_nse_session():
    global _session
    if _session is None:
        session = requests.Session()
        session.headers.update(HEADERS)
        session.get(NSE_BASE_URL, timeout=10)
        _session = session
    return _session
