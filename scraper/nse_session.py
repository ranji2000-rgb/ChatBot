# ChatBot/scraper/nse_session.py
import requests
import time

class NSESession:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.nseindia.com/option-chain",
            "Connection": "keep-alive",
        }
        self._warmup()

    def _warmup(self):
        self.session.get(
            "https://www.nseindia.com",
            headers=self.headers,
            timeout=5,
        )
        time.sleep(1)

    def get(self, url):
        return self.session.get(url, headers=self.headers, timeout=5)


# SINGLETON (IMPORTANT)
nse_session = NSESession()
