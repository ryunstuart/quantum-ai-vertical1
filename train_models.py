import pandas as pd
import xgboost as xgb
from lightgbm import LGBMRegressor, LGBMClassifier
import joblib

print("Loading data...")
df = pd.read_csv('synthetic_claims.csv')

# Features we will use (no leakage!)
features = ['member_age', 'billed_amount', 'days_since_injury', 
            'num_procedures', 'procedure_cpt', 'diagnosis_icd', 
            'claim_type', 'provider_id']

# Convert categorical columns
X = pd.get_dummies(df[features], drop_first=True)

print("Training 5 models...")

# 1. Fraud Model (Fixed - no actual_cost used)
fraud_model = xgb.XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42)
fraud_model.fit(X, df['fraud_flag'])
joblib.dump(fraud_model, 'model_fraud.pkl')

# 2. Predicted Cost
cost_model = xgb.XGBRegressor(n_estimators=300, max_depth=6, random_state=42)
cost_model.fit(X, df['actual_cost'])
joblib.dump(cost_model, 'model_costing.pkl')

# 3. Return-to-Work Days
rtw_model = LGBMRegressor(n_estimators=200, random_state=42)
rtw_model.fit(X, df['rtw_days'])
joblib.dump(rtw_model, 'model_forecasting.pkl')

# 4. Provider Score
score_model = LGBMRegressor(n_estimators=200, random_state=42)
score_model.fit(X, df['provider_score'])
joblib.dump(score_model, 'model_scoring.pkl')

# 5. Network Steering
steer_model = xgb.XGBClassifier(n_estimators=150, random_state=42)
steer_model.fit(X, df['steer_to_network'])
joblib.dump(steer_model, 'model_steering.pkl')

print("✅ All 5 models trained and saved successfully!")
print("You can now run the AI server.")