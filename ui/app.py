# ChatBot/ui/app.py
import sys
import os

# =========================================================
# FIX PYTHON PATH (CRITICAL)
# =========================================================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# =========================================================
# NOW IMPORT WORKS
# =========================================================
import streamlit as st

from scraper.option_chain_fetcher import fetch_option_chain
from parser.option_chain_parser import parse_option_chain
from analysis.oi_summary import generate_oi_summary

# =========================================================
# STREAMLIT UI
# =========================================================
st.set_page_config(page_title="Option Chain Analyzer", layout="wide")

st.title("📊 Option Chain Analyzer")
st.caption("NSE Option Chain (session-based, rate-limit safe)")

SYMBOLS = [
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
    "INFY",
    "TCS",
    "NIFTY",
    "BANKNIFTY",
]

symbol = st.selectbox("Select Symbol", SYMBOLS)

if st.button("Analyze", use_container_width=True):
    try:
        with st.spinner("Fetching option chain from NSE..."):
            raw_data = fetch_option_chain(symbol)

        df = parse_option_chain(raw_data)

        st.success("Option chain loaded successfully")
        st.dataframe(df, use_container_width=True)

        st.subheader("🧠 Open Interest Summary")
        summary = generate_oi_summary(df)
        for k, v in summary.items():
            st.write(f"**{k}:** {v}")

    except Exception as e:
        st.error("❌ Unable to fetch option chain from NSE")
        st.code(str(e))

st.markdown("---")
st.caption("Unofficial NSE data | For analysis only")
