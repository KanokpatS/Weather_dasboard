import dash
# from dash import dcc, html, Output, Input, State
# import dash_labs as dl
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Create navbar and dropdown for change page
navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
        ],
        nav=True,
        label="More Pages",
    ),
    brand="Thailand Weather Dashboard",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=False,
)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)