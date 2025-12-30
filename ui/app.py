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
st.caption("Data source: NSE (session-based fetch with retry & protection)")

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

symbol = st.selectbox(
    "Select Symbol",
    SYMBOLS,
    index=0
)

# =========================================================
# ANALYZE BUTTON
# =========================================================
if st.button("Analyze", use_container_width=True):
    try:
        with st.spinner("Fetching option chain from NSE..."):
            raw_data = fetch_option_chain(symbol)

        parsed_df = parse_option_chain(raw_data)

        st.success("Option chain fetched successfully")

        # -------------------------------------------------
        # OPTION CHAIN TABLE
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

            for key, value in oi_summary.items():
                st.write(f"**{key}:** {value}")

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
st.caption("For educational & analysis purposes only. NSE data is unofficial.")
