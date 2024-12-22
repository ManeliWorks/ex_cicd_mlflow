from ML.preprocess import preprocess_data
import joblib
import pandas as pd
import os

def predict_price(data):

    model_folder = 'ML'
    model_path = os.path.join(model_folder, 'xgb_model.pkl')
    scaler_path = os.path.join(model_folder, 'scaler.pkl')

    # Load the trained model
    model = joblib.load(model_path)

    # Load the scaler
    scaler = joblib.load(scaler_path)

    # Create DataFrame from input data
    input_df = pd.DataFrame(data)

    # Preprocess the input data
    processed_data = preprocess_data(input_df, scaler)

    # Predict the price
    predictions = model.predict(processed_data)

    # Return the predicted price
    return predictions[0]