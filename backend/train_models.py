import os, time, pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

os.makedirs('models', exist_ok=True)

df = pd.read_csv('health_risk_dataset.csv')
FEATURES = ['age','gender','bmi','bp_systolic','bp_diastolic','fasting_sugar',
            'hba1c','total_cholesterol','ldl','hdl','heart_rate',
            'smoking','alcohol','physical_activity','family_history']

X = df[FEATURES]
y = df['risk_level']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

MODELS = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Naive Bayes':         GaussianNB(),
    'Decision Tree':       DecisionTreeClassifier(max_depth=10, random_state=42),
    'Random Forest':       RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42),
    'SVM (Linear)':        SVC(kernel='linear', probability=True, random_state=42),
    'SVM (RBF)':           SVC(kernel='rbf', probability=True, random_state=42),
    'KNN':                 KNeighborsClassifier(n_neighbors=5),
}

CLASS_NAMES = ['Healthy', 'Low Risk', 'Moderate', 'High Risk']
results, conf_matrices = [], {}

print(f"{'Model':<22} {'Acc':>6} {'Prec':>6} {'Rec':>6} {'F1':>6} {'CV':>8} {'Time':>8}")
print("-" * 68)

for name, model in MODELS.items():
    t0 = time.time()
    model.fit(X_train_s, y_train)
    elapsed = time.time() - t0

    y_pred = model.predict(X_test_s)
    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec  = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1   = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    cv   = cross_val_score(model, X_train_s, y_train, cv=5, scoring='accuracy').mean()
    cm   = confusion_matrix(y_test, y_pred)

    results.append({'Model': name, 'Accuracy': round(acc,4), 'Precision': round(prec,4),
                    'Recall': round(rec,4), 'F1_Score': round(f1,4),
                    'CV_Score': round(cv,4), 'Training_Time': round(elapsed,3)})
    conf_matrices[name] = cm
    print(f"{name:<22} {acc:>6.4f} {prec:>6.4f} {rec:>6.4f} {f1:>6.4f} {cv:>8.4f} {elapsed:>7.3f}s")

results_df = pd.DataFrame(results).sort_values('Accuracy', ascending=False)
results_df.to_csv('model_comparison.csv', index=False)
print(f"\nBest model: {results_df.iloc[0]['Model']} ({results_df.iloc[0]['Accuracy']:.4f})")

# ── Comparison plots ─────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('ML Model Comparison – Health Risk Assessment', fontsize=14, fontweight='bold')
colors = plt.cm.Set2(np.linspace(0, 1, len(results_df)))
names  = results_df['Model'].tolist()

def hbar(ax, col, title, color):
    vals = results_df[col].tolist()
    bars = ax.barh(names, vals, color=colors)
    ax.set_xlim(min(vals)*0.95, 1.0)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(col)
    for bar, v in zip(bars, vals):
        ax.text(v + 0.001, bar.get_y() + bar.get_height()/2, f'{v:.4f}', va='center', fontsize=8)

hbar(axes[0,0], 'Accuracy',  'Accuracy Comparison',    colors)
hbar(axes[0,1], 'F1_Score',  'F1 Score Comparison',    colors)
hbar(axes[1,1], 'CV_Score',  'Cross-Validation Scores', colors)

# Training time (normal bar)
axes[1,0].bar(names, results_df['Training_Time'].tolist(), color=colors)
axes[1,0].set_title('Training Time (seconds)', fontweight='bold')
axes[1,0].set_ylabel('Seconds')
axes[1,0].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('model_comparison_plots.png', dpi=150, bbox_inches='tight')
plt.close()

# ── Confusion matrices ───────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 4, figsize=(18, 9))
fig.suptitle('Confusion Matrices – All 7 Models', fontsize=14, fontweight='bold')
axes_flat = axes.flatten()

for i, (name, cm) in enumerate(conf_matrices.items()):
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes_flat[i],
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    axes_flat[i].set_title(name, fontweight='bold', fontsize=9)
    axes_flat[i].set_xlabel('Predicted', fontsize=8)
    axes_flat[i].set_ylabel('Actual', fontsize=8)
    axes_flat[i].tick_params(axis='x', rotation=45, labelsize=7)
    axes_flat[i].tick_params(axis='y', rotation=0, labelsize=7)

axes_flat[-1].set_visible(False)
plt.tight_layout()
plt.savefig('confusion_matrices.png', dpi=150, bbox_inches='tight')
plt.close()

# ── Save Random Forest as deployment model ───────────────────────────────────
best_model = MODELS['Random Forest']
with open('models/best_model.pkl', 'wb') as f: pickle.dump(best_model, f)
with open('models/scaler.pkl', 'wb') as f:     pickle.dump(scaler, f)
with open('models/feature_names.pkl', 'wb') as f: pickle.dump(FEATURES, f)

print("Saved: models/best_model.pkl, models/scaler.pkl, models/feature_names.pkl")
print("Saved: model_comparison_plots.png, confusion_matrices.png")
