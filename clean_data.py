import pandas as pd
import numpy as np

def clean_product_dataset(df: pd.DataFrame):
    # Strip whitespace from 'date' column
    df.loc[:, 'date'] = df['date'].str.strip()
    
    # Drop duplicates based on 'date' column
    df.drop_duplicates(subset='date', inplace=True)

    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    # Set 'date' column as the index
    df.set_index('date', inplace=True)

    # Sort DataFrame by the index (date)
    df.sort_index(inplace=True)

    # Split 'retail_price_range_tk' into 'min_retail_price' and 'max_retail_price'
    if 'retail_price_range_tk' in df.columns and df['retail_price_range_tk'].str.contains("--").any():
        split_retail_price = df['retail_price_range_tk'].str.split("--", expand=True)
        df['min_retail_price'] = split_retail_price[0].fillna(np.nan).astype(float)
        df['max_retail_price'] = split_retail_price[1].fillna(np.nan).astype(float)
        df['avg_retail_price'] = (df['min_retail_price'] + df['max_retail_price']) / 2
    else:
        df['min_retail_price'] = np.nan
        df['max_retail_price'] = np.nan
        df['avg_retail_price'] = np.nan

    # Split 'wholesale_price_range_tk' into 'min_wholesale_price' and 'max_wholesale_price'
    if 'wholesale_price_range_tk' in df.columns and df['wholesale_price_range_tk'].str.contains("--").any():
        split_wholesale_price = df['wholesale_price_range_tk'].str.split("--", expand=True)
        df['min_wholesale_price'] = split_wholesale_price[0].fillna(np.nan).astype(float)
        df['max_wholesale_price'] = split_wholesale_price[1].fillna(np.nan).astype(float)
        df['avg_wholesale_price'] = (df['min_wholesale_price'] + df['max_wholesale_price']) / 2
    else:
        df['min_wholesale_price'] = np.nan
        df['max_wholesale_price'] = np.nan
        df['avg_wholesale_price'] = np.nan

    # Drop unnecessary columns
    df.drop(columns=['retail_price_range_tk', 'wholesale_price_range_tk'], inplace=True)

    # Generate a complete date range based on existing index
    date_range = pd.date_range(start=df.index.min(), end=df.index.max())

    # Reindex DataFrame to include all dates and fill missing values with NaN
    df = df.reindex(date_range)

    # Forward fill remaining NaN values in categorical columns
    df['product_group'].ffill(inplace=True)
    df['product_name_desc'].ffill(inplace=True)
    df['unit_retail'].ffill(inplace=True)
    df['unit_wholesale'].ffill(inplace=True)

    # Return the cleaned DataFrame with selected columns
    return df[['product_group', 'product_name_desc', 'unit_retail', 'min_retail_price', 'max_retail_price',
               'avg_retail_price', 'unit_wholesale', 'min_wholesale_price', 'max_wholesale_price', 'avg_wholesale_price']]
