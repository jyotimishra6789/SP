import pandas as pd
import numpy as np

# Load your augmented dataset
data = pd.read_csv("augmented_mouse_data.csv")

# Count existing fraud/trusted sessions
fraud_count = data[data['is_fraud'] == 1]['session_id'].nunique()
trusted_sessions = data[data['is_fraud'] == 0]['session_id'].unique()
trusted_count = len(trusted_sessions)

# Define how many fraud sessions you need to balance
needed = trusted_count - fraud_count

def simulate_fraud_on_session(df):
    df = df.copy()
    bot_type = np.random.choice(['linear', 'teleport', 'click_stamper'])
    
    n_points = len(df)
    
    if bot_type == 'linear':
        # Bot moving in a perfectly straight line at constant speed
        start_x, end_x = np.random.randint(0, 1920, 2)
        start_y, end_y = np.random.randint(0, 1080, 2)
        df['screen_x'] = np.linspace(start_x, end_x, n_points)
        df['screen_y'] = np.linspace(start_y, end_y, n_points)
        
        # Constant time interval between events (e.g. perfect 16ms loop)
        dt = np.random.choice([16.0, 32.0, 50.0])
        df['timestamp'] = df['timestamp'].iloc[0] + np.arange(n_points) * dt
        
    elif bot_type == 'teleport':
        # Instantly jumps across the screen in 0-1ms
        df['screen_x'] = np.random.randint(0, 1920, n_points)
        df['screen_y'] = np.random.randint(0, 1080, n_points)
        
        # The time delta between points is basically zero (impossible for humans)
        df['timestamp'] = df['timestamp'].iloc[0] + np.arange(n_points) * np.random.uniform(0.1, 1.0)
        
    elif bot_type == 'click_stamper':
        # Clicks extremely fast with unnatural patterns
        base_x = np.random.randint(0, 1920)
        base_y = np.random.randint(0, 1080)
        
        # Tiny tight cluster of movements
        df['screen_x'] = base_x + np.random.normal(0, 2, n_points)
        df['screen_y'] = base_y + np.random.normal(0, 2, n_points)
        
        # 1 = mousedown, 2 = mouseup. Simulates impossible 2ms click duration
        df['event_type'] = np.random.choice([1, 2], n_points)
        df['timestamp'] = df['timestamp'].iloc[0] + np.arange(n_points) * np.random.uniform(1.0, 5.0)

    df['is_fraud'] = 1
    return df

# Simulate additional fraud sessions
extra_fraud_data = pd.concat([
    simulate_fraud_on_session(data[data['session_id'] == sid])
    for sid in np.random.choice(trusted_sessions, size=needed, replace=True)
])

# Rename session IDs
extra_fraud_data['original_session_id'] = extra_fraud_data['session_id']
extra_fraud_data['session_id'] = 'fraud_' + extra_fraud_data['session_id'].astype(str)

# Final balanced dataset
balanced_df = pd.concat([data[data['is_fraud'] == 0], data[data['is_fraud'] == 1], extra_fraud_data])
balanced_df.to_csv("balanced_augmented_mouse_data.csv", index=False)

print("Balanced dataset saved as 'balanced_augmented_mouse_data.csv'")
print(balanced_df['is_fraud'].value_counts())
