# ui/app.py
import streamlit as st

from scraper.option_chain_fetcher import fetch_option_chain
from parser.option_chain_parser import parse_option_chain
from analysis.oi_summary import generate_oi_summary

# =========================================================
# STREAMLIT PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Option Chain Analyzer",
    layout="wide"
)

st.title("📊 Option Chain Analyzer")
st.caption("Data source: NSE (session-based fetch with retry protection)")

# =========================================================
# SYMBOL SELECTION
# =========================================================
SYMBOLS = [
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
    "INFY",
    "TCS",
    "NIFTY",
    "BANKNIFTY"
]

symbol = st.selectbox("Select Symbol", SYMBOLS)

# =========================================================
# ANALYZE BUTTON
# =========================================================
if st.button("Analyze", use_container_width=True):
    try:
        with st.spinner("Fetching option chain from NSE..."):
            raw_data = fetch_option_chain(symbol)

        parsed_df = parse_option_chain(raw_data)

        st.success("Option chain fetched successfully")

        st.subheader("📈 Option Chain Snapshot")
        st.dataframe(parsed_df, use_container_width=True)

        st.subheader("🧠 Open Interest Summary")
        try:
            summary = generate_oi_summary(parsed_df)
            for k, v in summary.items():
                st.write(f"**{k}:** {v}")
        except Exception as e:
            st.warning("OI summary failed")
            st.code(str(e))

    except Exception as e:
        st.error("❌ Unable to fetch option chain from NSE")
        st.warning("NSE rate-limit / session expired")
        st.code(str(e))

st.markdown("---")
st.caption("Unofficial NSE data. For analysis only.")
