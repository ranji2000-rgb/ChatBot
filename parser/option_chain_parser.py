from datetime import datetime

def parse_option_chain(raw_json: dict) -> dict:
    records = raw_json["records"]
    data = raw_json["filtered"]["data"]

    chain = {
        "symbol": records["underlying"],
        "spot": records["underlyingValue"],
        "expiry": records["expiryDates"][0],
        "timestamp": datetime.now().isoformat(),
        "strikes": []
    }

    for row in data:
        strike = row["strikePrice"]
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
