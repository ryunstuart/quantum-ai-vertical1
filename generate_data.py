import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n = 5000

claim_ids = range(1000001, 1000001 + n)
submission_times = [datetime(2024, 1, 1) + timedelta(hours=i) for i in range(n)]
member_ages = np.random.randint(18, 80, n)
member_genders = np.random.choice(['M', 'F'], n)
provider_ids = np.random.randint(100000, 999999, n)
billed_amounts = np.random.lognormal(7, 0.8, n).round(2)
procedure_cpts = np.random.choice(['99214', '97110', '99213', '97140', 'J1030', '99203'], n)
diagnosis_icds = np.random.choice(['M54.5', 'S39.012', 'M79.7', 'S13.4XXA', 'M54.2'], n)
claim_types = np.random.choice(['WorkersComp', 'Auto', 'Health', 'Liability'], n, p=[0.6, 0.25, 0.1, 0.05])
days_since_injury = np.random.randint(0, 365, n)
num_procedures = np.random.randint(1, 10, n)

fraud_prob = (billed_amounts > 2000).astype(float) * 0.3 + (days_since_injury < 10).astype(float) * 0.1 + np.random.rand(n)*0.05
fraud_flags = (np.random.rand(n) < fraud_prob).astype(int)

actual_costs = billed_amounts * (0.6 + np.random.rand(n)*0.3)
actual_costs = np.where(fraud_flags==1, actual_costs * 0.4, actual_costs).round(2)

rtw_days = np.random.randint(5, 120, n)
rtw_days = np.where(fraud_flags==1, rtw_days * 1.5, rtw_days).astype(int)

provider_scores = np.clip(0.5 + (np.random.rand(n) * 0.5) - (fraud_flags * 0.3), 0.1, 1.0).round(2)
steer_to_network = (provider_scores > 0.75).astype(int)

data = {
    'claim_id': claim_ids,
    'submission_timestamp': submission_times,
    'member_age': member_ages,
    'member_gender': member_genders,
    'provider_id': provider_ids,
    'billed_amount': billed_amounts,
    'procedure_cpt': procedure_cpts,
    'diagnosis_icd': diagnosis_icds,
    'claim_type': claim_types,
    'days_since_injury': days_since_injury,
    'num_procedures': num_procedures,
    'fraud_flag': fraud_flags,
    'actual_cost': actual_costs,
    'rtw_days': rtw_days,
    'provider_score': provider_scores,
    'steer_to_network': steer_to_network
}

df = pd.DataFrame(data)
df.to_csv('synthetic_claims.csv', index=False)
print("✅ Created synthetic_claims.csv with 5,000 fake claims!")