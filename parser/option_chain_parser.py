from datetime import datetime

def parse_option_chain(raw_json: dict) -> dict:
    # -------------------------------
    # SAFETY CHECK
    # -------------------------------
    if not raw_json or "records" not in raw_json:
        raise ValueError(
            f"NSE response invalid or blocked. Keys received: {list(raw_json.keys())}"
        )

    records = raw_json["records"]
    data = raw_json.get("filtered", {}).get("data", [])

    chain = {
        "symbol": records.get("underlying"),
        "spot": records.get("underlyingValue"),
        "expiry": records.get("expiryDates", [None])[0],
        "timestamp": datetime.now().isoformat(),
        "strikes": []
    }

    for row in data:
        strike = row.get("strikePrice")
        ce = row.get("CE", {})
        pe = row.get("PE", {})

        chain["strikes"].append({
            "strike": strike,
            "call": {
                "oi": ce.get("openInterest"),
                "oi_change": ce.get("changeinOpenInterest"),
                "ltp": ce.get("lastPrice"),
                "iv": ce.get("impliedVolatility")
            },
            "put": {
                "oi": pe.get("openInterest"),
                "oi_change": pe.get("changeinOpenInterest"),
                "ltp": pe.get("lastPrice"),
                "iv": pe.get("impliedVolatility")
            }
        })

    return chain
