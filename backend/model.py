import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib

# Load and sort data
data = pd.read_csv('augmented_mouse_data.csv')
data.sort_values(['session_id', 'timestamp'], inplace=True)

def extract_features(df):
    features = []
    for sid, group in df.groupby('session_id'):
        dx = group['screen_x'].diff().fillna(0)
        dy = group['screen_y'].diff().fillna(0)
        dt = group['timestamp'].diff().fillna(1)
        speed = np.sqrt(dx**2 + dy**2) / dt
        acc = speed.diff().fillna(0)

        clicks = group[group['event_type'] == 1]['timestamp']
        click_intervals = clicks.diff().dropna() / 1000

        time_span = (group['timestamp'].iloc[-1] - group['timestamp'].iloc[0]) / 1000
        num_events = len(group)
        event_clicks = (group['event_type'] == 1).sum()

        feature = {
            'avg_speed': speed.mean(),
            'max_speed': speed.max(),
            'min_speed': speed.min(),
            'std_speed': speed.std(),
            'acceleration_mean': acc.mean(),
            'acceleration_std': acc.std(),
            'curvature_mean': np.abs(dx / (dy + 1e-5)).mean(),
            'num_events': num_events,
            'event_clicks': event_clicks,
            'click_rate': event_clicks / time_span if time_span else 0,
            'time_span': time_span,
            'click_interval_mean': click_intervals.mean() if not click_intervals.empty else 0,
            'time_per_event': time_span / num_events if num_events else 0,
            'clicks_per_event': event_clicks / num_events if num_events else 0,
            'is_bot': group['is_fraud'].iloc[0]
        }
        features.append(feature)
    return pd.DataFrame(features)

features_df = extract_features(data)

# Feature selection
selected_features = [
    'avg_speed', 'max_speed', 'min_speed', 'std_speed',
    'acceleration_mean', 'acceleration_std', 'curvature_mean',
    'num_events', 'event_clicks', 'click_rate', 'time_span',
    'click_interval_mean', 'time_per_event', 'clicks_per_event'
]

X = features_df[selected_features]
y = features_df['is_bot']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

base_model = RandomForestClassifier(
    n_estimators=120, max_depth=10, class_weight='balanced_subsample', random_state=42
)
model = CalibratedClassifierCV(base_model, method='sigmoid', cv=3)
model.fit(X_train, y_train)

# Eval
print("\n🎯 Classification Report:\n")
print(classification_report(y_test, model.predict(X_test)))

# Save
joblib.dump(model, 'fraud_model_new.pkl')
joblib.dump((scaler, selected_features), 'scaler.pkl')
print("✅ Model and scaler saved.")
