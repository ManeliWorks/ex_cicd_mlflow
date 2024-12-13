
import pandas as pd


def preprocess_data(data, scaler):
    """
    Preprocess the input data to match the training data format.
    """


    # Define the columns used during training
    trained_columns = [
        'carat', 'cut', 'color', 'depth', 'table', 'x', 'y', 'z',
        'clarity_IF', 'clarity_SI1', 'clarity_SI2', 'clarity_VS1', 
        'clarity_VS2', 'clarity_VVS1', 'clarity_VVS2', 'volume'
    ]

    # Mapping categorical variables
    cut_mapping = {
        'Fair': 1,
        'Good': 2,
        'Very Good': 3,
        'Premium': 4,
        'Ideal': 5
    }
    color_mapping = {
        'D': 1,
        'E': 2,
        'F': 3,
        'G': 4,
        'H': 5,
        'I': 6,
        'J': 7
    }
    clarity_columns = ['clarity_IF', 'clarity_SI1', 'clarity_SI2', 'clarity_VS1', 
                       'clarity_VS2', 'clarity_VVS1', 'clarity_VVS2']

    # Apply mappings for 'cut' and 'color'
    data['cut'] = data['cut'].map(cut_mapping)
    data['color'] = data['color'].map(color_mapping)

    # One-hot encode 'clarity'
    clarity_dummies = pd.get_dummies(data['clarity'], prefix='clarity', drop_first=True)

    # Ensure all clarity columns are present, even if they have no data
    for col in clarity_columns:
        if col not in clarity_dummies.columns:
            clarity_dummies[col] = 0  # Add missing columns with default value 0

    # Convert clarity columns to boolean
    clarity_dummies = clarity_dummies.astype(bool)

    # Drop the 'clarity' column and concatenate the one-hot encoded columns
    data = pd.concat([data.drop('clarity', axis=1), clarity_dummies[clarity_columns]], axis=1)

    # Add a new feature for volume
    data['volume'] = data['x'] * data['y'] * data['z']

    # Ensure all columns match the trained model's features
    missing_cols = [col for col in trained_columns if col not in data.columns]
    for col in missing_cols:
        data[col] = 0  # Add missing columns with default value 0

    # Reorder the columns to match the trained model's feature order
    data = data[trained_columns]

    # Identify numeric features that were scaled during training
    numeric_features = ['carat', 'depth', 'table', 'volume']

    # Scale only the numeric features used during training
    data[numeric_features] = scaler.transform(data[numeric_features])

    return data
