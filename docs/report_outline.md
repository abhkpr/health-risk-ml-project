# Final Report Outline
## Smart Health Risk Assessment System

**Student:** Abhishek Kumar · CSJMA23001390288 · CSJMU Kanpur

---

### 1. Title Page
- Project name, student details, date: May 2025

### 2. Abstract
Problem: chronic disease burden in India. Approach: 7-algorithm ML ensemble on 2,000-patient dataset.
Result: 95.5% accuracy with Random Forest on 4-class risk prediction.

### 3. Introduction
- 77M diabetics, 54M CVD patients in India (WHO 2019)
- Preventive care gap in tier-2/3 cities
- Objectives: build, train, deploy and demonstrate ML risk assessment

### 4. Literature Review
- ML in healthcare (Kononenko 2001, Obermeyer & Emanuel 2016)
- Existing systems: CHA₂DS₂-VASc (cardio), FINDRISC (diabetes)
- Gaps: no integrated multi-disease risk + explainable web interface

### 5. Methodology
- Synthetic dataset generation (medical thresholds + feature-stratified noise)
- Feature engineering: 15 clinical and lifestyle variables
- Train-test split 80/20 stratified; StandardScaler
- 7 classifiers with hyperparameter rationale
- Metrics: accuracy, precision, recall, F1, 5-fold CV

### 6. Implementation
- Backend: Flask REST API, pickle-serialised model, CORS
- Frontend: Next.js App Router, Tailwind CSS, responsive form
- Deployment: Render (gunicorn) + Vercel (Next.js static + SSR)
- Screenshots: form, healthy result, high-risk result

### 7. Results & Analysis
- Model comparison table (see model_comparison.csv)
- Confusion matrices (7 models)
- Random Forest feature importance
- Best model selection: RF chosen for balance of accuracy + interpretability

### 8. Deployment & Demo
- Live URLs (Render + Vercel)
- API documentation (/health, /predict)
- End-to-end user flow

### 9. Conclusion & Future Scope
- Achieved 95.5% accuracy; deployed full-stack app
- Limitations: synthetic data, no temporal features
- Future: real EHR data, deep learning, mobile app, federated learning

### 10. References
1. WHO Global Health Estimates 2019
2. ICMR INDIAB Study
3. Scikit-learn: Pedregosa et al., JMLR 2011
4. Flask docs; Next.js docs
