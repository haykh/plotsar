import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import dash
import pandas as pd
import numpy as np

import json

from .defs import *
from .configs import *
from .physics import *
from .pulsar import PulsarCard


class Plotter:
    def __init__(self) -> None:
        self.app = None
        self.data = None
        self.data_units = None
        self.selected = {"x": None, "y": None, "col": None}
        self.loadData()

        self.x_dropdown = dash.html.Div(
            [
                dash.html.Span(
                    [
                        "x-axis",
                    ]
                ),
                dash.dcc.Dropdown(
                    list(plottable_columns_r.keys()),
                    value=plottable_columns["P0"],
                    multi=False,
                    searchable=False,
                    clearable=False,
                    id="x-select",
                ),
            ],
            className="multi-dropdown",
        )
        self.y_dropdown = dash.html.Div(
            [
                dash.html.Span(
                    [
                        "y-axis",
                    ]
                ),
                dash.dcc.Dropdown(
                    list(plottable_columns_r.keys()),
                    value=plottable_columns["P1"],
                    multi=False,
                    searchable=False,
                    clearable=False,
                    id="y-select",
                ),
            ],
            className="multi-dropdown",
        )
        self.col_dropdown = dash.html.Div(
            [
                dash.html.Span(
                    [
                        "color",
                    ]
                ),
                dash.dcc.Dropdown(
                    list(categorical_columns_r.keys()),
                    value=categorical_columns["Catalog"],
                    multi=False,
                    searchable=False,
                    clearable=False,
                    id="col-select",
                ),
            ],
            className="multi-dropdown",
        )

    def __del__(self) -> None:
        del self.data
        del self.data_units
        del self.app

    def loadData(self) -> None:
        del self.data
        data_fermi = json.load(open("plotly/data/fermi.json", "r"))
        data_atnf = json.load(open("plotly/data/atnf.json", "r"))
        units_atnf = {k: v[1] if v[1] != "" else None for k, v in data_atnf[0].items()}
        data_atnf = pd.DataFrame(
            {k: [d[k][0] for d in data_atnf] for k in data_atnf[0].keys()}
        )
        units_fermi = {
            k: v[1] if v[1] != "" else None for k, v in data_fermi[0].items()
        }
        data_fermi = pd.DataFrame(
            {k: [d[k][0] for d in data_fermi] for k in data_fermi[0].keys()}
        )
        data_atnf["Bsurf"] = ComputeBsurf(data_atnf)
        data_atnf["RLC"] = ComputeRLC(data_atnf)
        units_atnf["RLC"] = "km"
        data = pd.merge(
            data_fermi, data_atnf, on="Name", how="outer", indicator="Catalog"
        )
        data["Catalog"].replace(
            {"left_only": "Fermi", "right_only": "ATNF", "both": "Fermi"}, inplace=True
        )
        self.data = data.sort_values(by="Catalog", ascending=False)
        self.data_units = {**units_fermi, **units_atnf}

    def deploy(self, debug: bool = False, port: int = 8050) -> None:
        self.app = dash.Dash(
            __name__,
            external_stylesheets=external_stylesheets,
            external_scripts=external_scripts,
        )
        self.app.index_string = index_string
        self.app.layout = dash.html.Div(
            [
                dash.html.Div(
                    [self.x_dropdown, self.y_dropdown, self.col_dropdown],
                    className="toolbar",
                ),
                dash.html.Div(id="clientside-dummy"),
                dash.html.Div(
                    children=[
                        dash.dcc.Graph(
                            id="graph-main",
                            config={"displaylogo": False},
                        ),
                        dash.html.Div(
                            "Click on pulsar to display",
                            id="graph-info",
                        ),
                    ],
                    id="graph-datavis",
                ),
            ]
        )

        @self.app.callback(
            dash.Output("graph-info", "children"),
            dash.Input("graph-main", "clickData"),
        )
        def click_callback(clickData):
            if clickData is None:
                return "Click on pulsar to display"
            else:
                pt = clickData["points"][0]
                pulsar = self.data[
                    (self.data[self.selected["x"]] == pt["x"])
                    & (self.data[self.selected["y"]] == pt["y"])
                ]
                return PulsarCard(pulsar.iloc[0])

        @self.app.callback(
            dash.Output("graph-main", "figure"),
            dash.Input("x-select", "value"),
            dash.Input("y-select", "value"),
            dash.Input("col-select", "value"),
        )
        def update_graph(xaxis, yaxis, col) -> go.Figure:
            if xaxis == None or yaxis == None or col == None:
                labels = dict(x="x", y="y")
                fig = px.scatter(x=[0], y=[0], labels=labels)
            else:
                xaxis_word = xaxis
                yaxis_word = yaxis
                col_word = col
                xaxis = plottable_columns_r[xaxis]
                yaxis = plottable_columns_r[yaxis]
                col = categorical_columns_r[col]
                self.selected["x"] = xaxis
                self.selected["y"] = yaxis
                self.selected["col"] = col
                fig = px.scatter(
                    self.data,
                    x=xaxis,
                    y=yaxis,
                    color=np.log10(self.data[col]) if col != "Catalog" else col,
                )
                if col != "Catalog":
                    fig.update_layout(
                        coloraxis_colorbar=dict(
                            title=col_word,
                            title_side="top",
                            tickprefix="10<sup>",
                            ticksuffix="</sup>",
                            orientation="h",
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01,
                            thickness=15,
                        ),
                        coloraxis_colorscale="turbo",
                    )
                fig.update_traces(
                    marker_line_color="black",
                    marker_line_width=0.5,
                    marker_size=4,
                )
                fig.update_layout(
                    xaxis_title=to_label(xaxis_word, self.data_units[xaxis]),
                    yaxis_title=to_label(yaxis_word, self.data_units[yaxis]),
                    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                )
            fig.update_layout(layout_plotly)
            return fig

        pio.templates.default = "plotly_dark"
        self.app.run_server(debug=debug, port=port)
