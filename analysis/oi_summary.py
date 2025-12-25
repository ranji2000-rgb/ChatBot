def generate_oi_summary(chain: dict) -> dict:
    max_call = max(chain["strikes"], key=lambda x: x["call"]["oi"] or 0)
    max_put = max(chain["strikes"], key=lambda x: x["put"]["oi"] or 0)

    return {
        "symbol": chain["symbol"],
        "spot": chain["spot"],
        "max_call_oi": {
            "strike": max_call["strike"],
            "oi": max_call["call"]["oi"]
        },
        "max_put_oi": {
            "strike": max_put["strike"],
            "oi": max_put["put"]["oi"]
        }
    }
