from dash import Dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from layouts import home_layout, analyze_layout, predict_layout
from callbacks import register_callbacks

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
         dbc.Col(html.Img(src="./assets/logo/Price Flow.png", height="70px"), width="auto", className="d-flex align-items-center"),
       
        dbc.Col(
            [
                dbc.Button("Home", id="home-button", href="/", color="primary", className="me-1"),
                dbc.Button("Analyze", id="analyze-button", href="/analyze", color="primary", className="me-1"),
                dbc.Button("Predict", id="predict-button", href="/predict", color="secondary", className="me-1"),
            ],
            width="auto",
            className="d-flex justify-content-end align-items-center ms-auto"
        )
    ], align="center", style={'margin-bottom': '25px', 'margin-top': '15px'}),
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
], fluid=True, className="relative-container")

# Register callbacks
register_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
