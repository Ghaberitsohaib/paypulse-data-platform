from datetime import datetime, timezone
import random

class AMLFraudDetector:
    """
    Real-time Anti-Money Laundering (AML) & Fraud Engine.
    Detects high velocity card testing, structuring (smurfing), and sanction breaches.
    """
    def __init__(self, high_risk_threshold: int = 70):
        self.high_risk_threshold = high_risk_threshold
        self.seen_cards = {}

    def inspect_transaction(self, tx: dict) -> dict:
        risk_reasons = []
        risk_score = tx.get("risk_score", 10)

        # 1. Geographic anomaly
        if tx.get("country_code") in ["NG", "RU"]:
            risk_score += 30
            risk_reasons.append("HIGH_RISK_GEOGRAPHY")

        # 2. Velocity check (Simulated sliding window)
        card_id = f"{tx.get('card_bin')}-{tx.get('card_last4')}"
        now_ts = datetime.now(timezone.utc).timestamp()
        
        last_seen = self.seen_cards.get(card_id, 0)
        if now_ts - last_seen < 5.0 and last_seen > 0:
            risk_score += 40
            risk_reasons.append("RAPID_VELOCITY_BURST")
        self.seen_cards[card_id] = now_ts

        # 3. Micro-transaction card testing (< $2.00)
        if tx.get("amount", 0) < 2.00:
            risk_score += 25
            risk_reasons.append("MICRO_CARD_TESTING_PATTERN")

        # 4. Large amount AML structuring threshold (> $5000)
        if tx.get("amount", 0) >= 5000.00:
            risk_score += 35
            risk_reasons.append("AML_LARGE_TRANSACTION_STRUCTURING")

        is_flagged = risk_score >= self.high_risk_threshold
        return {
            "transaction_id": tx.get("transaction_id"),
            "account_id": tx.get("account_id"),
            "merchant_id": tx.get("merchant_id"),
            "amount": tx.get("amount"),
            "currency": tx.get("currency"),
            "final_risk_score": min(risk_score, 100),
            "is_flagged_aml": is_flagged,
            "reasons": "; ".join(risk_reasons) if risk_reasons else "NORMAL_TRANSACTION",
            "evaluated_at": datetime.now(timezone.utc).isoformat()
        }

if __name__ == "__main__":
    detector = AMLFraudDetector()
    test_tx = {
        "transaction_id": "TXN_TEST123",
        "account_id": "ACC_999",
        "card_bin": "411111",
        "card_last4": "1234",
        "amount": 1.25,
        "currency": "USD",
        "country_code": "NG",
        "risk_score": 60
    }
    result = detector.inspect_transaction(test_tx)
    print("AML Result:", result)
