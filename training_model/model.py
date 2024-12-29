import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
import os


def preprocess_and_reshape(df):
    melted_df = df.melt(id_vars=['date'], var_name='commodity', value_name='price')
    
    melted_df['commodity_type'] = melted_df['commodity'].str.extract(r'(.+)_avg_(.*)_price')[0]
    melted_df['price_type'] = melted_df['commodity'].str.extract(r'(.+)_avg_(.*)_price')[1]
    
    pivot_df = melted_df.pivot_table(index=['date', 'commodity_type'], columns='price_type', values='price')
    pivot_df = pivot_df.reset_index()
    
    pivot_df = pivot_df.interpolate(method='linear', axis=0).fillna(method='bfill').fillna(method='ffill')
    
    return pivot_df

def filter_columns(df, threshold=0.5):
    min_non_missing = len(df) * (1 - threshold)
    filtered_df = df.dropna(thresh=min_non_missing, axis=1)
    return filtered_df

def create_sequences(data, sequence_length):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i + sequence_length])
        y.append(data[i + sequence_length])
    return np.array(X), np.array(y)

from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def preprocess_for_lstm(df, sequence_length=30):
    numeric_df = df.select_dtypes(include=[float, int])  # Select only numeric columns

    if numeric_df.empty:
        raise ValueError("No numeric columns found in the DataFrame")

    scaler = MinMaxScaler(feature_range=(0, 1))

    scaled_data = scaler.fit_transform(numeric_df)

    X, y = create_sequences(scaled_data, sequence_length)

    return X, y, scaler


# Build complex LSTM model
def build_complex_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(100, return_sequences=True))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    model.add(LSTM(100, return_sequences=False))
    model.add(BatchNormalization())
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(25, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_and_save_models(data_path, models_path, sequence_length=30):
    os.makedirs(models_path, exist_ok=True)
    
    df = pd.read_csv(data_path)
    df_processed = preprocess_and_reshape(df)
    df_filtered = filter_columns(df_processed)
    
    commodities = df_filtered['commodity_type'].unique()
    for commodity in commodities:
        commodity_df = df_filtered[df_filtered['commodity_type'] == commodity]
        
        if commodity_df.shape[1] > 1:
            X, y, scaler = preprocess_for_lstm(commodity_df, sequence_length)
            input_shape = (X.shape[1], X.shape[2])
            
            model = build_complex_lstm_model(input_shape)
            model.fit(X, y, epochs=10, batch_size=32, validation_split=0.1)
            
            model_filename = os.path.join(models_path, f"{commodity}_model.h5")
            model.save(model_filename)
            print(f"Model for {commodity} saved to {model_filename}.")
        else:
            print(f"No sufficient data available for the selected commodity: {commodity}")

