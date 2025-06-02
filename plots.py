import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pydeck as pdk

def create_scatter_plot(data):
    """
    Create a scatter plot of GDP per capita vs Life Expectancy.
    """
    plot = px.scatter(data,
                     x="GDP per capita",
                     y="Life Expectancy (IHME)",
                     hover_data=["country"],
                     log_x=True,
                     size="Population",
                     color="country")
    return plot

def create_map_visualization(data, selected_metric, metric_options):
    """
    Create a map visualization using pydeck for 3D bars.
    """
    # Get the latest year's data for each country
    latest_data = data.sort_values('year').groupby('country').last().reset_index()
    
    # Calculate normalized values for bar heights
    # Use log scaling to emphasize differences
    min_value = latest_data[selected_metric].min()
    max_value = latest_data[selected_metric].max()
    
    # Add a small constant to avoid log(0)
    epsilon = 1e-10
    log_values = np.log(latest_data[selected_metric] + epsilon)
    log_min = np.log(min_value + epsilon)
    log_max = np.log(max_value + epsilon)
    
    # Normalize to 0-1 range and scale up
    normalized_values = (log_values - log_min) / (log_max - log_min)
    latest_data['normalized_value'] = normalized_values * 5000  # Increased scale factor
    
    # Create the pydeck layer
    layer = pdk.Layer(
        'ColumnLayer',
        data=latest_data,
        get_position=['longitude', 'latitude'],
        get_elevation='normalized_value',
        elevation_scale=100,  # Increased elevation scale
        radius=50000,
        get_fill_color=[255, 0, 0, 140],  # Red color with some transparency
        pickable=True,
        auto_highlight=True,
    )
    
    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=0,
        latitude=0,
        zoom=1,
        pitch=45,
        bearing=0
    )
    
    # Create the deck.gl map
    deck = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer],
        tooltip={
            'html': f'''
                <b>Country:</b> {{country}}<br/>
                <b>{metric_options[selected_metric]}:</b> {{{selected_metric}:.2f}}<br/>
                <b>Log-scaled value:</b> {{{{normalized_value:.2f}}}}
            ''',
            'style': {
                'backgroundColor': 'white',
                'color': 'black',
                'padding': '10px'
            }
        }
    )
    
    return deck

# Define metric options as a constant
METRIC_OPTIONS = {
    "Life Expectancy (IHME)": "Life Expectancy (years)",
    "GDP per capita": "GDP per capita ($)",
    "Population": "Population",
    "headcount_ratio_upper_mid_income_povline": "Poverty Rate (%)"
} 