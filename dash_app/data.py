import pandas as pd

# Function to load data from the selected product group
def load_data(product_group):
    filepath = f'./data/merged_category_wise_data/{product_group}.csv'
    df = pd.read_csv(filepath, parse_dates=['date'])
    return df

# Function to clean column names
def clean_column_name(col):
    if '_avg_retail_price' in col:
        return col.replace('_avg_retail_price', '')
    elif '_avg_wholesale_price' in col:
        return col.replace('_avg_wholesale_price', '')
    return col

# Create a mapping of shorter labels to original column names
def create_label_mapping(df):
    label_mapping = {}
    for col in df.columns:
        if 'avg_retail_price' in col or 'avg_wholesale_price' in col:
            short_label = clean_column_name(col)
            label_mapping[short_label] = col
    return label_mapping
