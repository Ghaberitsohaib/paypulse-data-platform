import json
import time
import random
import uuid
from datetime import datetime, timezone

CARD_NETWORKS = ["VISA", "MASTERCARD", "AMEX"]
CURRENCIES = ["USD", "EUR", "GBP", "MAD"]
COUNTRIES = ["US", "MA", "FR", "GB", "DE", "AE", "NG", "RU"]
HIGH_RISK_COUNTRIES = ["NG", "RU"]

def generate_payment_event(is_fraud: bool = False):
    """Generates an ISO-like payment authorization event with idempotency keys."""
    card_brand = random.choice(CARD_NETWORKS)
    bin_prefix = {"VISA": "411111", "MASTERCARD": "550000", "AMEX": "370000"}[card_brand]
    card_last4 = f"{random.randint(1000, 9999)}"
    
    country = random.choice(HIGH_RISK_COUNTRIES) if is_fraud else random.choice(COUNTRIES)
    
    if is_fraud:
        # Suspicious micro-testing or sudden massive spike
        amount = random.choice([0.99, 1.25, 4999.00, 9850.00])
        status = "FLAGGED_REVIEW" if amount > 2000 else "APPROVED"
    else:
        amount = round(random.uniform(5.00, 450.00), 2)
        status = "APPROVED" if random.random() > 0.08 else "DECLINED"

    return {
        "transaction_id": f"TXN_{uuid.uuid4().hex[:12].upper()}",
        "idempotency_key": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "account_id": f"ACC_{random.randint(100, 999)}",
        "merchant_id": f"MERCH_{random.randint(1, 15):04d}",
        "card_brand": card_brand,
        "card_bin": bin_prefix,
        "card_last4": card_last4,
        "amount": amount,
        "currency": random.choice(CURRENCIES),
        "status": status,
        "country_code": country,
        "risk_score": random.randint(75, 99) if is_fraud else random.randint(1, 35),
        "ip_address": f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
    }

def run_producer(num_events: int = 50, delay_sec: float = 0.05):
    print(f"[Producer] Emitting {num_events} payment stream events to Kafka...")
    events = []
    for i in range(num_events):
        fraud_bias = (i % 7 == 0)
        event = generate_payment_event(is_fraud=fraud_bias)
        events.append(event)
        time.sleep(delay_sec)
    print(f"[Producer] Successfully emitted {len(events)} transactions!")
    return events

if __name__ == "__main__":
    sample = run_producer(10, 0.01)
    print("Sample Event:", json.dumps(sample[0], indent=2))
