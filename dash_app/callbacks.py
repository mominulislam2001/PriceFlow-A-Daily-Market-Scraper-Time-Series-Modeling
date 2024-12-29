from dash import dcc, html, Input, Output
import plotly.express as px
from data import load_data, create_label_mapping, clean_column_name
from layouts import home_layout, analyze_layout, predict_layout

def register_callbacks(app):
    # Callback to render page content based on URL
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/predict':
            return predict_layout
        elif pathname == '/analyze':
            return analyze_layout
        return home_layout  # Default to home_layout

    # Callback to update product options based on selected product group
    @app.callback(
        [Output('retail-price-dropdown', 'options'),
         Output('retail-price-dropdown', 'value'),
         Output('wholesale-price-dropdown', 'options'),
         Output('wholesale-price-dropdown', 'value')],
        [Input('product-group-dropdown', 'value')]
    )
    def update_product_options(selected_group):
        df = load_data(selected_group)
        label_mapping = create_label_mapping(df)
        retail_columns = [col for col in df.columns if 'avg_retail_price' in col]
        wholesale_columns = [col for col in df.columns if 'avg_wholesale_price' in col]
        retail_options = [{'label': clean_column_name(col), 'value': col} for col in retail_columns]
        wholesale_options = [{'label': clean_column_name(col), 'value': col} for col in wholesale_columns]
        return retail_options, [retail_columns[0]], wholesale_options, [wholesale_columns[0]]

    # Callback to update the retail price chart based on selected products
    @app.callback(
        Output('retail-price-chart', 'figure'),
        [Input('product-group-dropdown', 'value'),
         Input('retail-price-dropdown', 'value')]
    )
    def update_retail_chart(selected_group, selected_retail_products):
        df = load_data(selected_group)
        fig = px.line(df, x='date', y=selected_retail_products, title="Retail Price")
        fig.update_layout(legend_title_text='Products')
        fig.for_each_trace(lambda t: t.update(name=clean_column_name(t.name)))
        return fig

    # Callback to update the wholesale price chart based on selected products
    @app.callback(
        Output('wholesale-price-chart', 'figure'),
        [Input('product-group-dropdown', 'value'),
         Input('wholesale-price-dropdown', 'value')]
    )
    def update_wholesale_chart(selected_group, selected_wholesale_products):
        df = load_data(selected_group)
        fig = px.line(df, x='date', y=selected_wholesale_products, title="Wholesale Prices")
        fig.update_layout(legend_title_text='Products')
        fig.for_each_trace(lambda t: t.update(name=clean_column_name(t.name)))
        return fig

    # Callback to update the retail price histogram based on selected products
    @app.callback(
        Output('retail-price-histogram', 'figure'),
        [Input('product-group-dropdown', 'value'),
         Input('retail-price-dropdown', 'value')]
    )
    def update_retail_histogram(selected_group, selected_retail_products):
        df = load_data(selected_group)
        df_melted = df.melt(id_vars=['date'], value_vars=selected_retail_products, var_name='Product', value_name='Price')
        fig = px.histogram(df_melted, x='Price', color='Product', barmode='overlay', title="Distribution of Retail Prices")
        return fig

    # Callback to update the wholesale price histogram based on selected products
    @app.callback(
        Output('wholesale-price-histogram', 'figure'),
        [Input('product-group-dropdown', 'value'),
         Input('wholesale-price-dropdown', 'value')]
    )
    def update_wholesale_histogram(selected_group, selected_wholesale_products):
        df = load_data(selected_group)
        df_melted = df.melt(id_vars=['date'], value_vars=selected_wholesale_products, var_name='Product', value_name='Price')
        fig = px.histogram(df_melted, x='Price', color='Product', barmode='overlay', title="Distribution of Wholesale Prices")
        return fig

    # Callback to update button styles based on URL
    @app.callback(
        Output("home-button", "style"),
        Output("analyze-button", "style"),
        Output("predict-button", "style"),
        Input("url", "pathname")
    )
    def update_button_styles(pathname):
        # Define default and active colors
        active_color = "#205079"
        default_color = "#1EA3D6"

        # Define button styles
        home_style = {"backgroundColor": active_color if pathname == "/" else default_color, "borderColor": default_color}
        analyze_style = {"backgroundColor": active_color if pathname == "/analyze" else default_color, "borderColor": default_color}
        predict_style = {"backgroundColor": active_color if pathname == "/predict" else default_color, "borderColor": default_color}

        return home_style, analyze_style, predict_style
