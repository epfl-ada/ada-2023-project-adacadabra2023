from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Seasonal analysis of beerstyles per country'),
    dcc.Graph(id="pie-charts-x-graph"),
    html.P("Names:"),
    dcc.Dropdown(id='pie-charts-x-names',
        options=['1st', '2nd', '3rd', '4th'],
        value='Season', clearable=False
    ),
    html.P("Values:"),
    dcc.Dropdown(id='pie-charts-x-values',
        options=['total_bill', 'tip', 'size'],
        value='Country', clearable=False
    ),
])


@app.callback(
    Output("pie-charts-x-graph", "figure"), 
    Input("pie-charts-x-names", "value"), 
    Input("pie-charts-x-values", "value"))
def generate_chart(names, values):
    df = px.data.tips() # replace with your own data source
    fig = px.pie(df, values=values, names=names, hole=.3)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
