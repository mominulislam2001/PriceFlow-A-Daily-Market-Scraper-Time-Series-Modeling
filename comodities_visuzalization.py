import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
import glob 


def basic_statistics(df_dict,comodities):
    for comodity in comodities:
        print("\nBasic Statistics:\n",df_dict[comodity].describe())
        print("\nMissing Values:\n", df_dict[comodity].isnull().sum())

def visualize_trends(df_dict, commodities, price_type='retail'):
    combined_df = pd.DataFrame()
    for commodity in commodities:
        commodity_data = df_dict[commodity].copy()
        commodity_data['commodity'] = commodity
        combined_df = pd.concat([combined_df, commodity_data])
    
    if price_type == 'retail':
        y_column = 'avg_retail_price'
        title = 'Average Retail Price Trends of Selected Commodities'
    elif price_type == 'wholesale':
        y_column = 'avg_wholesale_price'
        title = 'Average Wholesale Price Trends of Selected Commodities'
        
    fig = px.line(combined_df, x=combined_df.index, y=y_column, color='commodity',
                  title=title,
                  labels={y_column: 'Price', 'index': 'Date', 'commodity': 'Commodity'})
    fig.show()
    
def load_folder_dataframe_in_dictionary(path):  
    oil_df_dict  = dict()
    list_of_csv = os.listdir(path)
    for csv in list_of_csv:
        oil_df = pd.read_csv(f"{path}/{csv}",index_col=0, parse_dates=True)
        oil_df_dict[csv.strip('.csv')] = oil_df
        
    return oil_df_dict


def visualize_price_distribution(df_dict, commodities, price_type='retail'):
    fig = go.Figure()
    
    for commodity in commodities:
        fig.add_trace(go.Box(
            y=df_dict[commodity][f'avg_{price_type}_price'],
            name=commodity,
            boxpoints='all',  # Display all points
            jitter=0.5,       # Add some jitter for better visibility
            whiskerwidth=0.2  # Narrower whiskers to highlight outliers
        ))
    
    fig.update_layout(
        title=f'Distribution of Average {price_type.capitalize()} Prices',
        xaxis_title='Commodity',
        yaxis_title=f'Average {price_type.capitalize()} Price',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        boxmode='group',  # Group boxes for each commodity
        height=1600,       # Adjust height of the plot
        width=1200        # Adjust width of the plot
    )
    
    fig.show()
def visualize_price_histogram(df_dict, commodities, price_type='retail'):
    fig = go.Figure()
    
    for commodity in commodities:
        fig.add_trace(go.Histogram(
            x=df_dict[commodity][f'avg_{price_type}_price'],
            name=commodity,
            opacity=0.5
        ))
    
    fig.update_layout(
        title=f'Histogram of Average {price_type.capitalize()} Prices',
        xaxis_title=f'Average {price_type.capitalize()} Price',
        yaxis_title='Frequency',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=1600,       # Adjust height of the plot
        width=1200        # Adjust width of the plot
    )
    
    fig.show()


def get_folder_commodities_list(path):
    list_of_csv = os.listdir(path)
    name_list = []
    for csv in list_of_csv:
        name_list.append(csv.strip('.csv'))
        
    return name_list



