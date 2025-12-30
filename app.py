# app.py
import streamlit as st
import requests
import time
import pandas as pd

# =========================================================
# NSE SESSION (TAKEN FROM WORKING ZIP LOGIC)
# =========================================================
@st.cache_resource
def create_nse_session():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/option-chain",
        "Connection": "keep-alive",
    }
    session.headers.update(headers)

    # Warm-up (CRITICAL)
    session.get("https://www.nseindia.com", timeout=5)
    time.sleep(1)

    return session


# =========================================================
# OPTION CHAIN FETCHER (DIRECT & SAFE)
# =========================================================
def fetch_option_chain(symbol):
    session = create_nse_session()

    symbol = symbol.upper()

    if symbol in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"]:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    else:
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"

    for _ in range(3):
        resp = session.get(url, timeout=5)
        if resp.status_code == 200:
            try:
                data = resp.json()
                if "records" in data:
                    return data
            except Exception:
                pass
        time.sleep(1)

    raise Exception("NSE blocked or invalid response")


# =========================================================
# PARSER
# =========================================================
def parse_option_chain(data):
    rows = []
    for item in data["records"]["data"]:
        ce = item.get("CE", {})
        pe = item.get("PE", {})
        rows.append({
            "Strike": item.get("strikePrice"),
            "CE_OI": ce.get("openInterest"),
            "CE_LTP": ce.get("lastPrice"),
            "PE_LTP": pe.get("lastPrice"),
            "PE_OI": pe.get("openInterest"),
        })
    return pd.DataFrame(rows)


# =========================================================
# OI SUMMARY
# =========================================================
def oi_summary(df):
    ce = df["CE_OI"].sum()
    pe = df["PE_OI"].sum()
    pcr = round(pe / ce, 2) if ce else None

    return {
        "Total CE OI": ce,
        "Total PE OI": pe,
        "PCR": pcr,
        "Bias": "Bullish" if pcr and pcr > 1 else "Bearish"
    }


# =========================================================
# STREAMLIT UI
# =========================================================
st.set_page_config(page_title="NSE Option Chain", layout="wide")

st.title("📊 NSE Option Chain Analyzer")
st.caption("Built from scratch using proven NSE session logic")

symbol = st.selectbox(
    "Select Symbol",
    ["RELIANCE", "HDFCBANK", "ICICIBANK", "INFY", "TCS", "NIFTY", "BANKNIFTY"]
)

if st.button("Analyze", use_container_width=True):
    try:
        with st.spinner("Fetching data from NSE..."):
            raw = fetch_option_chain(symbol)
            df = parse_option_chain(raw)

        st.success("Option chain loaded")
        st.dataframe(df, use_container_width=True)

        st.subheader("🧠 OI Summary")
        summary = oi_summary(df)
        for k, v in summary.items():
            st.write(f"**{k}:** {v}")

    except Exception as e:
        st.error("Failed to fetch option chain")
        st.code(str(e))

st.markdown("---")
st.caption("Unofficial NSE data • For analysis only")
