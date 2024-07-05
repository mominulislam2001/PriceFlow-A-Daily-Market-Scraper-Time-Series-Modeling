import pandas as pd
import numpy as np

def replace_outliers(series):
    # Calculate the absolute difference of each timepoint from the series mean
    absolute_differences_from_mean = np.abs(series - np.mean(series))
    
    # Calculate a mask for the differences that are > 3 standard deviations from zero
    outlier_mask = absolute_differences_from_mean > (np.std(series) * 3)
    
    # Replace these values with the median across the data
    series[outlier_mask] = np.nanmedian(series)
    
    return series

def handle_outliers(df_dict, commodities, price_type='retail', method='median'):
    for commodity in commodities:
        data = df_dict[commodity][f'avg_{price_type}_price']
        
        # Apply the chosen method to replace outliers
        if method == 'median':
            data = replace_outliers(data)
        # Add other methods here if needed in the future
        
        # Update the dataframe in the dictionary
        df_dict[commodity][f'avg_{price_type}_price'] = data
    
    return df_dict