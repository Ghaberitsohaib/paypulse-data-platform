import random
from datetime import datetime, timezone

def generate_mock_merchants(count: int = 10):
    """Simulates merchant KYC registry from a Core Banking REST API."""
    categories = [
        ("MCC_5411", "Grocery & Supermarkets", 0.015, 0.03),
        ("MCC_5812", "Restaurants & Dining", 0.022, 0.05),
        ("MCC_5732", "Electronics & Gadgets", 0.025, 0.07),
        ("MCC_4722", "Travel & Airlines", 0.028, 0.10),
        ("MCC_7995", "Online Gaming & Betting", 0.035, 0.15)
    ]
    
    merchants = []
    for i in range(1, count + 1):
        mcc_code, mcc_name, fee_rate, reserve_pct = random.choice(categories)
        merchants.append({
            "merchant_id": f"MERCH_{i:04d}",
            "legal_name": f"Enterprise Partner {i:03d} LLC",
            "mcc_code": mcc_code,
            "category_name": mcc_name,
            "country_code": random.choice(["US", "MA", "FR", "GB", "DE", "AE"]),
            "interchange_rate": fee_rate,
            "reserve_holdback_rate": reserve_pct,
            "payout_schedule": "DAILY_NET_D1",
            "kyc_verified": True,
            "registered_at": datetime.now(timezone.utc).isoformat()
        })
    return merchants

def fetch_mock_fx_rates():
    """Simulates Central Bank Daily Foreign Exchange Rates API."""
    return [
        {"base_currency": "USD", "target_currency": "USD", "exchange_rate": 1.0000, "rate_date": datetime.now(timezone.utc).strftime("%Y-%m-%d")},
        {"base_currency": "USD", "target_currency": "EUR", "exchange_rate": 0.9250, "rate_date": datetime.now(timezone.utc).strftime("%Y-%m-%d")},
        {"base_currency": "USD", "target_currency": "GBP", "exchange_rate": 0.7920, "rate_date": datetime.now(timezone.utc).strftime("%Y-%m-%d")},
        {"base_currency": "USD", "target_currency": "MAD", "exchange_rate": 10.150, "rate_date": datetime.now(timezone.utc).strftime("%Y-%m-%d")},
        {"base_currency": "USD", "target_currency": "AED", "exchange_rate": 3.6725, "rate_date": datetime.now(timezone.utc).strftime("%Y-%m-%d")}
    ]

if __name__ == "__main__":
    print(f"Generated {len(generate_mock_merchants())} merchants.")
    print("FX Rates:", fetch_mock_fx_rates())
