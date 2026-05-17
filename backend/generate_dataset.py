import numpy as np
import pandas as pd

np.random.seed(42)
N = 2000

# Generate features biased by risk class so they're more discriminative
labels = np.array([0]*500 + [1]*600 + [2]*500 + [3]*400)
np.random.shuffle(labels)

def feature_by_risk(low, high, label, spread=None):
    base = low + (high - low) * (label / 3)
    # Generous noise so adjacent classes overlap realistically
    noise = spread if spread else (high - low) * 0.35
    return np.random.normal(base, noise)

age             = np.array([feature_by_risk(22, 75, l, 12) for l in labels]).clip(20, 85).astype(int)
gender          = np.random.randint(0, 2, N)
bmi             = np.array([feature_by_risk(20, 40, l, 5) for l in labels]).clip(15, 50).round(1)
bp_systolic     = np.array([feature_by_risk(110, 175, l, 18) for l in labels]).clip(90, 190).astype(int)
bp_diastolic    = np.array([feature_by_risk(68, 105, l, 12) for l in labels]).clip(60, 115).astype(int)
fasting_sugar   = np.array([feature_by_risk(80, 240, l, 35) for l in labels]).clip(70, 260).astype(int)
hba1c           = np.array([feature_by_risk(4.5, 11.5, l, 1.5) for l in labels]).clip(4.0, 12.5).round(1)
total_cholesterol = np.array([feature_by_risk(150, 290, l, 45) for l in labels]).clip(130, 310).astype(int)
ldl             = np.array([feature_by_risk(70, 195, l, 35) for l in labels]).clip(60, 210).astype(int)
hdl             = np.array([feature_by_risk(75, 30, l, 18) for l in labels]).clip(25, 95).astype(int)
heart_rate      = np.array([feature_by_risk(62, 100, l, 15) for l in labels]).clip(50, 115).astype(int)
smoking         = np.array([1 if np.random.rand() < 0.1 + 0.2*(l/3) else 0 for l in labels])
alcohol         = np.array([1 if np.random.rand() < 0.1 + 0.15*(l/3) else 0 for l in labels])
physical_activity = np.array([feature_by_risk(6, 1, l, 1) for l in labels]).clip(0, 7).round().astype(int)
family_history  = np.array([1 if np.random.rand() < 0.15 + 0.25*(l/3) else 0 for l in labels])

df = pd.DataFrame({
    'age': age, 'gender': gender, 'bmi': bmi,
    'bp_systolic': bp_systolic, 'bp_diastolic': bp_diastolic,
    'fasting_sugar': fasting_sugar, 'hba1c': hba1c,
    'total_cholesterol': total_cholesterol, 'ldl': ldl, 'hdl': hdl,
    'heart_rate': heart_rate, 'smoking': smoking, 'alcohol': alcohol,
    'physical_activity': physical_activity, 'family_history': family_history,
    'risk_level': labels
})

df.to_csv('health_risk_dataset.csv', index=False)
print(f"Dataset saved: {len(df)} records")
print(df['risk_level'].value_counts().sort_index().rename({0:'Healthy',1:'Low',2:'Moderate',3:'High'}))
