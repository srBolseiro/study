''' Intended result: Displaying line charts.
    Requires 2 args: filename (.csv) and LimitOfRows (int)'''
from sys import argv
from dash import Dash, dcc, Input, Output, callback
from dash import html as h
from pandas import read_csv
from plotly_express import line, bar


# Argv
if len(argv) != 3:
    exit("Usage: dashboard.py 'filename.csv' 'LimitOfRows'")

# Flask setting
app = Dash(__name__)

# Load dataframe
try:
    df = read_csv(argv[1], nrows=int(argv[2]))
except:
    exit("Invalid input")

# Html
app.layout = h.Section([
    h.Div(dcc.Dropdown(options=[{"label": "PnL", "value": "pnl"}, {"label": "Cash Flow", "value":"cashflow"}], 
                       placeholder="Choose the value", id="chartValueDrop", clearable=False), className="dropdown"),
    h.Div(dcc.Dropdown(options=[{"label": "TS", "value": "ts"}],
                        placeholder="xAxis", id="chartXDrop",  clearable=False), className="dropdown"),
    h.Article(dcc.Graph(id="mainChart"))
], className="center")

# Charts
def drawChart(dataframe, type, xAxis, yAxis):
    match type:
        case "line":
            chartGraph = line(dataframe, x=xAxis, y=yAxis)
        case "bar":
            chartGraph = bar(dataframe, x=xAxis, y=yAxis)
        case _:
            return line(None)
    return chartGraph

# Handle input
@callback(
        Output(component_id="mainChart", component_property="figure"),
        Input(component_id="chartValueDrop", component_property="value"),
        Input(component_id="chartXDrop", component_property="value")
)
def select_value(value, x):
    if not value or not x:
        chart = drawChart(None, None, None, None)
        return chart
    else:
        chart = drawChart(df, "line", xAxis=x, yAxis=value)
        return chart

# Flask setting
if __name__ == '__main__':
    app.run(debug=True)
