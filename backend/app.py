from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

model = joblib.load("fraud_model_new.pkl")
scaler, selected_features = joblib.load("scaler.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("📥 Incoming data:", data)

        input_df = pd.DataFrame([data])
        input_df = input_df[selected_features]
        scaled = scaler.transform(input_df)

        trust_score = model.predict_proba(scaled)[0][1]
        prediction = int(model.predict(scaled)[0])
        label = "Human ✅" if prediction == 1 else "Bot ❌"

        return jsonify({
            "success": True,
            "trust_score": round(trust_score, 4),
            "prediction": prediction,
            "label": label
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == "__main__":
    print("🚀 Server running at http://127.0.0.1:5000")
    app.run(debug=True)
