
import pandas as pd
import os
import glob
from clean_data import clean_product_dataset
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def get_individual_product_dataset_subf(df: pd.DataFrame, save_path: str):
    product_group_list = df['product_group'].unique()

    for product_group in product_group_list:
        # Create a folder for the product group if it doesn't exist
        group_folder = os.path.join(save_path, product_group)
        os.makedirs(group_folder, exist_ok=True)
        
        # Filter by product group
        group_df = df[df['product_group'] == product_group]
        
        # Get unique product names within the product group
        product_name_list = group_df['product_name_desc'].unique()

        for product_name in product_name_list:
            # Replace invalid characters in the filename
            safe_product_name = product_name.replace('/', '_')  # Replace '/' with '_'
            product_df = group_df[group_df['product_name_desc'] == product_name]
            clean_product_df = clean_product_dataset(product_df)

            # Save cleaned data to CSV within the product group folder
            csv_path = os.path.join(group_folder, f'{safe_product_name}.csv')
            clean_product_df.to_csv(csv_path)


if __name__ == "__main__":
    
    df = pd.read_csv('./merged_data/final_merged_data.csv')
  
    df.drop(columns=['Serial Number'],inplace=True)
  
    df.rename(columns={
    
    "Product Group":"product_group",
    "Product Name and Description":"product_name_desc",
    "Unit Retail":"unit_retail",
    "Retail Price (Tk) Lowest Price - Highest Price":"retail_price_range_tk",
    "Unit Wholesale":"unit_wholesale",
    "Wholesale Price (Tk) Lowest Price - Highest Price":"wholesale_price_range_tk",
    "Price Date":"date"
    
           },inplace=True)
    
    
    get_individual_product_dataset_subf(df,'./cleaned_product_wise_data')
    