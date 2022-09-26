import dash

dash.register_page(__name__, path='/', name='Map')

import pandas as pd
import geopandas as gpd
from datetime import date

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly import graph_objs as go

def get_province_data() -> pd.DataFrame:
    """
    Creat thailand map dataframe (name and geometry of province) from file
    :return: Thailand map dataframe
    """
    thai_map_df = gpd.read_file("dashboard/data/THA_MAP.shp")
    province_name = pd.read_csv("dashboard/data/Province_NAME.csv", index_col=None)
    province_name["NAME"] = province_name["NAME"].apply(lambda x: x.replace("\t", ""))

    thai_map_df["จังหวัด"] = province_name["NAME"]
    thai_map_df["Province"] = province_name["Province"]
    thai_map_df['centroid'] = thai_map_df.geometry.apply(lambda x: x.centroid)
    thai_map_df['longitude'] = thai_map_df.centroid.x
    thai_map_df['latitude'] = thai_map_df.centroid.y
    thai_map_df = thai_map_df.sort_values(by="จังหวัด")
    return thai_map_df

def preprocess_data(thai_map_df: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean weather data and map merge thailand map dataframe on province
    :param thai_map_df: Thailand map dataframe
    :param df: Weather dataframe from scrape.py
    :return: Combined dataframe merged on on province
    """
    df['จังหวัด'] = df['จังหวัด'].replace(
        ['ชัยนาท สกษ.', 'สมุทรปราการ สกษ.', 'อุบลราชธานี (ศูนย์ฯ)', 'พิจิตร สกษ.', 'ปทุมธานี สกษ.', 'พัทลุง สกษ.', 'ยะลา สกษ.'],
        ['ชัยนาท', 'สมุทรปราการ', 'อุบลราชธานี', 'พิจิตร', 'ปทุมธานี', 'พัทลุง', 'ยะลา'])
    df['rain'] = df['rain'].replace(['ไม่มีฝน', 'ฝนเล็กน้อย'], 0)
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
    df['temp_high'] = df['temp_high'].astype(float)
    df['temp_low'] = df['temp_low'].astype(float)
    df['wind'] = df['wind'].astype(float)
    df['rain'] = df['rain'].astype(float)
    df_all = thai_map_df.merge(df, on='จังหวัด', how='left')
    return df_all

def find_average_value(df: pd.DataFrame) -> pd.DataFrame:
    """
    Find average value of weather group by province
    :param df: Combined dataframe or filter dataframe
    :return: Aggregate dataframe
    """
    df_summary = df.groupby(['จังหวัด', 'Province'])\
        .agg(avg_temp_high=('temp_high', 'mean'),
             avg_temp_low=('temp_low', 'mean'), avg_wind=('wind', 'mean'), avg_rain=('rain', 'mean'))
    df_summary = df_summary.reset_index()
    return df_summary

# Prepare data for dashboard
df = pd.read_excel('dashboard/data/weather_data.xlsx')
thai_map = get_province_data()
df = preprocess_data(thai_map, df)
th_json = "https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json"

def plot_map(df_agg: pd.DataFrame, filtered_province_df: pd.DataFrame, selected_data: str):
    """
    Plot thailand map for feature that selected
    :param df_agg: Aggregate dataframe
    :param filtered_province_df: Weather that filter by province
    :param selected_data: Feature that selected
    :return: Thailand map
    """
    fig_map = px.choropleth_mapbox(df_agg, geojson=th_json, locations='Province', color=f'avg_{selected_data}',
                                   featureidkey="properties.name",
                                   color_continuous_scale='Viridis',
                                   labels={'avg_temp_high': 'high temperature'},
                                   center={"lat": 13.036717, "lon": 100.523186},
                                   mapbox_style="carto-positron",
                                   zoom=5
                                   )
    fig_map_dot = go.Figure(go.Scattermapbox(
        lat=filtered_province_df['latitude'],
        lon=filtered_province_df['longitude'],
        marker=dict(color=list(range(6)),
                    colorscale='viridis',
                    size=16)
    ))
    fig_map.add_trace(fig_map_dot.data[0])
    for i, frame in enumerate(fig_map.frames):
        fig_map.frames[i].data += (fig_map_dot.frames[i].data[0],)
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_map

def plot_line_graph(filtered_province_df: pd.DataFrame, selected_data:str):
    """
    Plot line graph for feature that selected
    :param filtered_province_df: Weather that filter by province
    :param selected_data: Feature that selected
    :return: Line plot
    """
    fig_line = px.line(filtered_province_df, x='date', y=selected_data,
                       labels={'temp_high': 'high temperature', 'temp_low': 'low temperature'})
    return fig_line

layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.Div([
                    dcc.Graph(id='map',style={'height': '73vh'})
                ], className='class2 card'), width={'size': 6, 'order': 1}),
                dbc.Col(html.Div([
                    html.Label("Province", style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'},
                               className='dropdown-labels'),
                    dcc.Dropdown(df['Province'].unique(), 'Bangkok Metropolis', id='selected_province'),
                    html.Label("Display Data", style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'},
                               className='dropdown-labels'),
                    dcc.Dropdown(
                        options={
                            'temp_high': 'high temperature',
                            'temp_low': 'low temperature',
                            'wind': 'wind',
                            'rain': 'rain'
                        },
                        value='temp_high', id='selected_data'),
                    html.Label("Date", style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'},
                               className='date-labels'),
                    dcc.DatePickerRange(
                        id='date-range',
                        min_date_allowed=date(2022, 7, 1),
                        max_date_allowed=date(2022, 8, 31),
                        initial_visible_month=date(2022, 8, 31),
                        start_date=date(2022, 7, 1),
                        end_date=date(2022, 8, 31)
                    ),
                    dcc.Graph(id='graph')
                ], className='class2 card', style={'margin-left': '1px', 'text-align': 'center'}),
                    width={'size': 6, 'order': 2})
            ])
        ], style={'background-color': '#F7F8FE', 'padding': '20px'})
    ])

@callback(
    Output('graph', 'figure'),
    Output('map', 'figure'),
    Input('selected_province', 'value'),
    Input('selected_data', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_graph(selected_province, selected_data, start_date, end_date):
    filtered_date_df = df[df.date <= end_date]
    filtered_date_df = filtered_date_df[filtered_date_df.date >= start_date]
    filtered_province_df = filtered_date_df[filtered_date_df.Province == selected_province]
    fig_line = plot_line_graph(filtered_province_df, selected_data)
    df_agg = find_average_value(filtered_date_df)
    fig_map = plot_map(df_agg, filtered_province_df, selected_data)
    return fig_line, fig_map