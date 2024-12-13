from preprocess import preprocess_data
import joblib
import pandas as pd


# Load the trained model
model = joblib.load('xgb_model.pkl')

# Load the scaler
scaler = joblib.load('scaler.pkl')

print("Model and Scaler loaded successfully!")

# Fake data for testing
fake_data = {
    'carat': [0.23],  # Example carat size
    'cut': ['Ideal'],  # Example cut quality
    'color': ['E'],  # Example color grade
    'clarity': ['SI2'],  # Example clarity grade
    'depth': [61.5],  # Example depth
    'table': [55],  # Example table size
    'x': [3.95],  # Example x dimension
    'y': [3.98],  # Example y dimension
    'z': [2.43]   # Example z dimension
}

# Create DataFrame from fake data
fake_df = pd.DataFrame(fake_data)

# Preprocess the fake data
processed_fake_data = preprocess_data(fake_df, scaler)

# Predict the price
predictions = model.predict(processed_fake_data)

# Output the predicted price
print("Predicted Price for Fake Data:", predictions[0])