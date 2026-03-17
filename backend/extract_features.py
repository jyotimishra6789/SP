import pandas as pd
import numpy as np

# Load your balanced session data
df = pd.read_csv("balanced_augmented_mouse_data.csv")

# Ensure numeric timestamps
df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce').fillna(0)

# Extract features per session
feature_rows = []

for session_id, group in df.groupby("session_id"):
    group = group.sort_values("timestamp")

    dx = group['screen_x'].diff().fillna(0)
    dy = group['screen_y'].diff().fillna(0)
    dt = group['timestamp'].diff().fillna(0.01)

    speed = np.sqrt(dx**2 + dy**2) / dt
    speed.replace([np.inf, -np.inf], 0, inplace=True)

    features = {
        "session_id": session_id,
        "avg_speed": speed.mean(),
        "max_speed": speed.max(),
        "click_rate": (group['event_type'] == 1).sum() / len(group),
        "erratic_moves": ((np.abs(dx) > 50) | (np.abs(dy) > 50)).sum(),
        "is_fraud": group['is_fraud'].iloc[0]
    }

    feature_rows.append(features)

# Save extracted features
features_df = pd.DataFrame(feature_rows)
features_df.to_csv("session_features.csv", index=False)

print("✅ Features extracted to 'session_features.csv'")
print(features_df.head())
