import joblib

model = joblib.load('fraud_model_new.pkl')
scaler = joblib.load('scaler.pkl')

# Sample inputs: [avg_speed, max_speed, num_events, event_clicks]
samples = [
    [45, 130, 35, 8],   # likely human
    [15, 80, 12, 1],    # likely bot
]

for i, features in enumerate(samples):
    scaled = scaler.transform([features])
    score = model.predict_proba(scaled)[0][1]
    pred = model.predict(scaled)[0]
    label = "Human ✅" if pred == 1 else "Bot ❌"
    print(f"Sample {i+1} → Trust Score: {score:.2%} → {label}")
