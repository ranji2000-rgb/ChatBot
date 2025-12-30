# ui/app.py
import streamlit as st

from scraper.option_chain_fetcher import fetch_option_chain
from parser.option_chain_parser import parse_option_chain
from analysis.oi_summary import generate_oi_summary
from config.symbols import SYMBOLS if False else None  # safe import placeholder

# =========================================================
# STREAMLIT PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Option Chain Analyzer",
    layout="wide"
)

st.title("📊 Option Chain Analyzer")

st.caption(
    "Data source: NSE (session-based fetch with retry & protection against rate limits)"
)

# =========================================================
# SYMBOL SELECTION
# =========================================================
DEFAULT_SYMBOLS = [
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
    "INFY",
    "TCS",
    "NIFTY",
    "BANKNIFTY"
]

symbol = st.selectbox(
    "Select Symbol",
    DEFAULT_SYMBOLS,
    index=0
)

# =========================================================
# ANALYZE BUTTON
# =========================================================
if st.button("Analyze", use_container_width=True):
    try:
        with st.spinner("Fetching option chain from NSE..."):
            raw_data = fetch_option_chain(symbol)

        # -------------------------------------------------
        # PARSE OPTION CHAIN
        # -------------------------------------------------
        parsed_df = parse_option_chain(raw_data)

        st.success("Option chain fetched successfully")

        # -------------------------------------------------
        # DISPLAY TABLE
        # -------------------------------------------------
        st.subheader("📈 Option Chain Snapshot")
        st.dataframe(
            parsed_df,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # OI SUMMARY
        # -------------------------------------------------
        st.subheader("🧠 Open Interest Summary")

        try:
            oi_summary = generate_oi_summary(parsed_df)

            for k, v in oi_summary.items():
                st.write(f"**{k}:** {v}")

        except Exception as e:
            st.warning("OI summary could not be generated")
            st.code(str(e))

    except Exception as e:
        st.error("❌ Unable to fetch option chain from NSE")
        st.warning("Possible reasons: NSE rate-limit, session expiry, or network block")
        st.code(str(e))

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption("Built for educational & analysis purposes. NSE data is unofficial.")
