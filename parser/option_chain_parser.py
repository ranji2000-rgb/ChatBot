# ChatBot/parser/option_chain_parser.py
import pandas as pd

def parse_option_chain(raw_data):
    records = raw_data["records"]["data"]

    rows = []
    for item in records:
        strike = item.get("strikePrice")

        ce = item.get("CE", {})
        pe = item.get("PE", {})

        rows.append({
            "Strike": strike,
            "CE_OI": ce.get("openInterest"),
            "CE_LTP": ce.get("lastPrice"),
            "PE_LTP": pe.get("lastPrice"),
            "PE_OI": pe.get("openInterest"),
        })

    return pd.DataFrame(rows)
