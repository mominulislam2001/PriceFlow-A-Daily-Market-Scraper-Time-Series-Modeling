from dash import dcc, html
import dash_bootstrap_components as dbc
import os

# List available product groups
product_groups = [f.split('.')[0] for f in os.listdir('./data/merged_category_wise_data/') if f.endswith('.csv')]

# Home layout
home_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("About This Project"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.P("This project provides a comprehensive dashboard for analyzing commodity prices. The dashboard allows users to view trends and distributions for both retail and wholesale prices across various product groups."), width=12),
    ]),
    dbc.Row([
        dbc.Col(html.P("Created by: Md. Mominul Islam"), width=12),
        dbc.Col(html.P("Contact: islamayan123456@gmail.com"), width=12),
    ]),
    dbc.Row([
        dbc.Col(html.P("Usage: This tool can be used for market analysis, pricing strategy formulation, and understanding price trends in various commodity categories."), width=12),
    ])
], fluid=True)

# Analyze layout
analyze_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Label("Select Product Group"), width=4),
        dbc.Col(html.Label("Select Retail Products"), width=4),
        dbc.Col(html.Label("Select Wholesale Products"), width=4)
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='product-group-dropdown',
                options=[{'label': pg, 'value': pg} for pg in product_groups],
                value=product_groups[0],
                style={'margin-bottom': '17px'}
            ), width=4
        ),
        dbc.Col(
            dcc.Dropdown(
                id='retail-price-dropdown',
                options=[],
                multi=True,
                style={'margin-bottom': '17px'}
            ), width=4
        ),
        dbc.Col(
            dcc.Dropdown(
                id='wholesale-price-dropdown',
                options=[],
                multi=True,
                style={'margin-bottom': '17px'}
            ), width=4
        )
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='retail-price-chart',
            style={
                'height': '300px',
                'borderRadius': '50px',  # Rounded borders
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',  # Shadow
                'backgroundColor': '#fff'  # Optional: background color to make shadow more visible
            }
        ), width=6),
        dbc.Col(dcc.Graph(
            id='wholesale-price-chart',
            style={
                'height': '300px',
                'borderRadius': '50px',  # Rounded borders
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',  # Shadow
                'backgroundColor': '#fff'  # Optional: background color to make shadow more visible
            }
        ), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='retail-price-histogram',
            style={
                'height': '300px',
                'borderRadius': '50px',  # Rounded borders
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',  # Shadow
                'backgroundColor': '#fff'  # Optional: background color to make shadow more visible
            }
        ), width=6),
        dbc.Col(dcc.Graph(
            id='wholesale-price-histogram',
            style={
                'height': '300px',
                'borderRadius': '50px',  # Rounded borders
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',  # Shadow
                'backgroundColor': '#fff'  # Optional: background color to make shadow more visible
            }
        ), width=6)
    ])
], fluid=True)

# Predict layout (Placeholder)
predict_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Prediction Page"), width=12)
    ]),
    # Add your prediction components here, with similar styles if needed
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='prediction-chart',
            style={
                'height': '300px',
                'borderRadius': '50px',  # Rounded borders
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',  # Shadow
                'backgroundColor': '#fff'  # Optional: background color to make shadow more visible
            }
        ), width=12)
    ])
], fluid=True)
