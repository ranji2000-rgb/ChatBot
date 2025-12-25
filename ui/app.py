import streamlit as st
import json

from scraper.option_chain_fetcher import fetch_option_chain
from parser.option_chain_parser import parse_option_chain
from analysis.oi_summary import generate_oi_summary

# Load symbols
with open("config/symbols.json") as f:
    symbols = json.load(f)

st.set_page_config(page_title="Option Chain Bot", layout="wide")

st.title("📊 Option Chain Analyzer")

symbol = st.selectbox("Select Symbol", sorted(symbols.keys()))

if st.button("Analyze"):
    with st.spinner("Fetching option chain..."):
        raw = fetch_option_chain(symbol)
        chain = parse_option_chain(raw)
        summary = generate_oi_summary(chain)

    st.subheader("Summary")
    st.json(summary)

    st.subheader("Raw Option Chain (Parsed)")
    st.dataframe(chain["strikes"])
