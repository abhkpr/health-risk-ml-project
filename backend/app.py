import os, pickle, numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

def load_pickle(name):
    with open(os.path.join(MODEL_DIR, name), 'rb') as f:
        return pickle.load(f)

try:
    model         = load_pickle('best_model.pkl')
    scaler        = load_pickle('scaler.pkl')
    feature_names = load_pickle('feature_names.pkl')
    MODEL_LOADED  = True
except Exception as e:
    MODEL_LOADED = False
    print(f"[WARN] Could not load model: {e}")

RISK_LABELS = {0: 'Healthy', 1: 'Low Risk', 2: 'Moderate Risk', 3: 'High Risk'}
RISK_COLORS = {0: '#22c55e', 1: '#eab308', 2: '#f97316', 3: '#ef4444'}

RECOMMENDATIONS = {
    0: [
        "Maintain your healthy lifestyle – you're doing great!",
        "Continue regular exercise (150+ min/week of moderate activity).",
        "Annual comprehensive health checkup recommended.",
        "Stay hydrated and maintain a balanced diet."
    ],
    1: [
        "Monitor blood pressure and sugar levels monthly.",
        "Increase physical activity to 30 min/day.",
        "Schedule a doctor visit every 6 months.",
        "Reduce sodium and processed food intake."
    ],
    2: [
        "Lifestyle changes are required – act now.",
        "Check vitals weekly (BP, blood sugar, weight).",
        "Consult a nutritionist for a personalised diet plan.",
        "Avoid smoking and limit alcohol consumption.",
        "Doctor visit every 3 months."
    ],
    3: [
        "URGENT: Please see your doctor immediately.",
        "Daily monitoring of blood pressure and blood glucose.",
        "Strict medication compliance – do not skip doses.",
        "Avoid all tobacco and alcohol.",
        "Consider specialist referral (cardiologist / endocrinologist).",
        "Emergency contacts should be kept handy."
    ]
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'model_loaded': MODEL_LOADED,
        'features': feature_names if MODEL_LOADED else [],
        'algorithms': 7
    })

@app.route('/predict', methods=['POST'])
def predict():
    if not MODEL_LOADED:
        return jsonify({'error': 'Model not loaded'}), 503

    data = request.get_json(force=True)

    # Validate all features present
    missing = [f for f in feature_names if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    try:
        values = np.array([[float(data[f]) for f in feature_names]])
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid input: {e}'}), 400

    scaled   = scaler.transform(values)
    risk_code = int(model.predict(scaled)[0])
    probs     = model.predict_proba(scaled)[0].tolist()
    confidence = round(float(probs[risk_code]) * 100, 1)

    prob_map = {RISK_LABELS[i]: round(p * 100, 1) for i, p in enumerate(probs)}

    return jsonify({
        'risk_level':      RISK_LABELS[risk_code],
        'risk_code':       risk_code,
        'confidence':      confidence,
        'color':           RISK_COLORS[risk_code],
        'recommendations': RECOMMENDATIONS[risk_code],
        'probabilities':   prob_map
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
