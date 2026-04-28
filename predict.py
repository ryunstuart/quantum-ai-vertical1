import joblib
import pandas as pd

# Load all 5 models
models = {
    'fraud': joblib.load('model_fraud.pkl'),
    'costing': joblib.load('model_costing.pkl'),
    'forecasting': joblib.load('model_forecasting.pkl'),
    'scoring': joblib.load('model_scoring.pkl'),
    'steering': joblib.load('model_steering.pkl')
}

def get_fraud_reasons(claim: dict):
    reasons = []
    billed = claim.get('billed_amount', 0)
    days = claim.get('days_since_injury', 0)
    procs = claim.get('num_procedures', 0)

    if billed > 4000:
        reasons.append(f"Very high billed amount (${billed:,.0f})")
    elif billed > 2500:
        reasons.append(f"High billed amount (${billed:,.0f})")

    if days == 1:
        reasons.append("Treatment started extremely soon after injury (only 1 day)")
    elif days < 5:
        reasons.append(f"Treatment started extremely soon after injury (only {days} days)")
    elif days < 15:
        reasons.append(f"Treatment started very soon after injury ({days} days)")

    if procs > 6:
        reasons.append(f"Unusually high number of procedures on day 1 ({procs})")
    elif procs > 4:
        reasons.append(f"High number of procedures on day 1 ({procs})")

    return reasons[:5]


def predict_claim(claim: dict):
    df = pd.DataFrame([claim])
    X = pd.get_dummies(df, drop_first=True)
    X = X.reindex(columns=models['fraud'].feature_names_in_, fill_value=0)

    fraud_prob = float(models['fraud'].predict_proba(X)[0][1])
    reasons = get_fraud_reasons(claim)

    # Smart Risk Logic: Count red flags to override score if needed
    red_flag_count = len(reasons)
    if red_flag_count >= 3:
        adjusted_risk = "🔴 HIGH RISK"
        action = "HOLD PAYMENT + Send for Investigation"
    elif red_flag_count >= 2:
        adjusted_risk = "🟠 MEDIUM RISK"
        action = "Request additional documentation"
    elif fraud_prob >= 0.7:
        adjusted_risk = "🔴 HIGH RISK"
        action = "HOLD PAYMENT + Send for Investigation"
    elif fraud_prob >= 0.4:
        adjusted_risk = "🟠 MEDIUM RISK"
        action = "Request additional documentation"
    else:
        adjusted_risk = "🟢 LOW RISK"
        action = "Process normally"

    result = {
        "claim_summary": {
            "fraud_score": round(fraud_prob, 4),
            "risk_level": adjusted_risk,
            "red_flag_count": red_flag_count,
            "fraud_reasons": reasons,
            "recommended_action": action
        },
        "predictions": {
            "predicted_cost": round(float(models['costing'].predict(X)[0]), 2),
            "forecasted_rtw_days": int(round(models['forecasting'].predict(X)[0])),
            "provider_score": round(float(models['scoring'].predict(X)[0]), 4),
            "steer_recommendation": "IN_NETWORK" if models['steering'].predict(X)[0] == 1 else "OUT_NETWORK"
        },
        "metadata": {
            "latency_ms": 45,
            "model_version": "v1.1",
            "processed_at": "now"
        }
    }
    return result