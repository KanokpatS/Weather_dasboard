import dash

dash.register_page(__name__, name='Summary')

import pandas as pd
import geopandas as gpd

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px

dash.register_page(__name__)

def get_province_data() -> pd.DataFrame:
    """

    :return:
    """
    thai_map_df = gpd.read_file("data/THA_MAP.shp")
    province_name = pd.read_csv("data/Province_NAME.csv", index_col=None)
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

    :param thai_map_df:
    :param df:
    :return:
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

    :param df:
    :return:
    """
    df_summary = df.groupby(['จังหวัด', 'Province'])\
        .agg(avg_temp_high=('temp_high', 'mean'),
             avg_temp_low=('temp_low', 'mean'), avg_wind=('wind', 'mean'), avg_rain=('rain', 'mean'))
    df_summary = df_summary.reset_index()
    return df_summary

# Prepare data for dashboard
df = pd.read_excel('data/weather_data.xlsx')
thai_map = get_province_data()
df = preprocess_data(thai_map, df)
th_json = "https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json"

def plot_line_graph_temp(filtered_province_df):

    fig_line = px.line(filtered_province_df, x='date', y='temp_high',
                       labels={'temp_high': 'high temperature', 'temp_low': 'low temperature'})
    fig_line.add_scatter(x=filtered_province_df['date'], y=filtered_province_df['temp_low'], mode='lines')
    return fig_line

def plot_line_graph(filtered_province_df, selected_data):
    fig_line = px.line(filtered_province_df, x='date', y=selected_data)
    return fig_line

layout = html.Div([
        dbc.Container([
            html.Label("Select Province", style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'},
                       className='dropdown-labels'),
            dcc.Dropdown(df['Province'].unique(), 'Bangkok Metropolis', id='selected_province'),
            dbc.Row([

                dbc.Col(html.Div([
                    # html.P(
                    #     f"This is the disk usage on \
                    #          per user, \
                    #         as of ."
                    # ),
                    html.Label("Temperature", style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'},
                               className='other-labels'),
                    dcc.Graph(id='temp')
                ], className='class2 card'), style={'text-align': 'center'}, width={'size': 6, 'order': 1}),
                dbc.Col(html.Div([
                    html.Label("Wind", style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'},
                               className='other-labels'),
                    dcc.Graph(id='wind'),
                    html.Label("Rain", style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'},
                               className='other-labels'),
                    dcc.Graph(id='rain')
                ], className='class2 card', style={'margin-left': '1px', 'text-align': 'center'}),
                    width={'size': 6, 'order': 2})
            ], style={'padding': '20px'})
        ], style={'background-color': '#F7F8FE', 'padding': '5px'})
    ])

@callback(
    Output('temp', 'figure'),
    Output('wind', 'figure'),
    Output('rain', 'figure'),
    Input('selected_province', 'value')
)
def update_graph(selected_province):
    filtered_province_df = df[df.Province == selected_province]
    fig_temp = plot_line_graph_temp(filtered_province_df)
    fig_wind = plot_line_graph(filtered_province_df, 'wind')
    fig_rain = plot_line_graph(filtered_province_df, 'rain')
    return fig_temp, fig_wind, fig_rain
