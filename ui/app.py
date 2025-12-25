import sys
import os
import json
import streamlit as st

# ======================================================
# FIX PYTHON PATH (CRITICAL FOR STREAMLIT CLOUD)
# ======================================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # ChatBot/
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# ======================================================
# IMPORT INTERNAL MODULES
# ======================================================
from scraper.option_chain_fetcher import fetch_option_chain
from parser.option_chain_parser import parse_option_chain
from analysis.oi_summary import generate_oi_summary

# ======================================================
# LOAD SYMBOLS (ABSOLUTE PATH)
# ======================================================
SYMBOLS_FILE = os.path.join(BASE_DIR, "config", "symbols.json")

with open(SYMBOLS_FILE, "r") as f:
    symbols = json.load(f)

# ======================================================
# STREAMLIT UI
# ======================================================
st.set_page_config(page_title="Option Chain Bot", layout="wide")
st.title("📊 Option Chain Analyzer")

symbol = st.selectbox("Select Symbol", sorted(symbols.keys()))

if st.button("Analyze"):
    with st.spinner("Fetching option chain..."):
        raw = fetch_option_chain(symbol)
        chain = parse_option_chain(raw)
        summary = generate_oi_summary(chain)

    st.subheader("📌 OI Summary")
    st.json(summary)

    st.subheader("📄 Parsed Option Chain")
    st.dataframe(chain["strikes"])
