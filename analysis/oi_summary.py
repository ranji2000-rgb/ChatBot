# ChatBot/analysis/oi_summary.py
def generate_oi_summary(df):
    ce_oi = df["CE_OI"].sum()
    pe_oi = df["PE_OI"].sum()

    pcr = round(pe_oi / ce_oi, 2) if ce_oi else None

    bias = "Bullish" if pcr and pcr > 1 else "Bearish"

    return {
        "Total CE OI": ce_oi,
        "Total PE OI": pe_oi,
        "PCR": pcr,
        "Market Bias": bias,
    }
