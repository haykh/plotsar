import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import dash
import pandas as pd
import numpy as np

from num2tex import num2tex
from num2tex import configure as num2tex_configure

num2tex_configure(exp_format="cdot", help_text=False, display_singleton=False)

import json

from .defs import *
from .physics import *


def to_label(label, unit):
    return f"{label} [{unit}]" if unit else label


def exp_tex(float_number):
    ret = "{:.2g}".format(num2tex(float_number))
    if ret.startswith("\cdot"):
        ret = ret.replace("\cdot", "")
    return ret


layout_plotly = go.Layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis={
        "zerolinecolor": "rgba(255,255,255,0.45)",
        "exponentformat": "power",
        "tickcolor": "rgba(255,255,255,0.45)",
        "tickwidth": 0.5,
        "ticklen": 5,
        "ticks": "inside",
        "type": "log",
        "gridwidth": 0.25,
        "gridcolor": "rgba(255,255,255,0.05)",
    },
    yaxis={
        "zerolinecolor": "rgba(255,255,255,0.45)",
        "exponentformat": "power",
        "tickcolor": "rgba(255,255,255,0.45)",
        "tickwidth": 0.5,
        "ticklen": 5,
        "ticks": "inside",
        "type": "log",
        "gridwidth": 0.1,
        "gridcolor": "rgba(255,255,255,0.05)",
    },
    uirevision="constant",
    modebar={"orientation": "h"},
    font_family="JetBrains Mono",
)
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com",
        "rel": "preconnect",
    },
    {
        "href": "https://fonts.gstatic.com",
        "rel": "preconnect",
        "crossorigin": "anonymous",
    },
    {
        "href": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,800;1,400&display=swap",
        "rel": "stylesheet",
    },
]
external_scripts = [
    "https://polyfill.io/v3/polyfill.min.js?features=es6",
]


def PulsarCard(pulsar):
    if pulsar["P0"] < 0.1:
        period = rf"$P = {{{exp_tex(pulsar['P0'] * 1000)}}}~\textrm{{ms}}$"
    else:
        period = rf"$P = {{{exp_tex(pulsar['P0'])}}}~\textrm{{s}}$"
    pdot = rf"\(\dot{{P}} = {{{exp_tex(pulsar['P1'])}}}\)"
    rlc = rf"$R_{{\rm LC}} = {{{exp_tex(pulsar['RLC'])}}}~\textrm{{km}}$"
    bstar = rf"$B_* = {{{exp_tex(pulsar['Bsurf'])}}}~\textrm{{G}}$"
    edot = rf"$\dot{{E}} = {{{exp_tex(pulsar['Edot'])}}}~\textrm{{erg/s}}$"
    return [
        dash.html.H1(pulsar["Name"]),
        dash.html.P(period),
        dash.html.P(pdot),
        dash.html.P(bstar),
        dash.html.P(edot),
        dash.html.P(rlc),
    ]


class Plotter:
    def __init__(self) -> None:
        self.app = None
        self.data = None
        self.data_units = None
        self.loadData()

        self.x_dropdown = dash.html.Div(
            [
                dash.html.Span(
                    [
                        "x-axis",
                    ]
                ),
                dash.dcc.Dropdown(
                    list(plottable_columns.keys()),
                    value="P0",
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
                    list(plottable_columns.keys()),
                    value="P1",
                    multi=False,
                    searchable=False,
                    clearable=False,
                    id="y-select",
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
            {"left_only": "Fermi", "right_only": "ATNF", "both": "Both"}, inplace=True
        )
        self.data = data
        self.data_units = {**units_fermi, **units_atnf}

    def deploy(self, debug: bool = False, port: int = 8050) -> None:
        self.app = dash.Dash(
            __name__,
            external_stylesheets=external_stylesheets,
            external_scripts=external_scripts,
        )
        self.app.layout = dash.html.Div(
            [
                dash.html.Div(
                    [
                        self.x_dropdown,
                        self.y_dropdown,
                    ],
                    className="toolbar",
                ),
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
                take_data = self.data[
                    ~((self.data["Catalog"] == "ATNF") ^ (pt["curveNumber"] == 0))
                ]
                pulsar = take_data.iloc[pt["pointNumber"]]
                return PulsarCard(pulsar)

        @self.app.callback(
            dash.Output("graph-main", "figure"),
            dash.Input("x-select", "value"),
            dash.Input("y-select", "value"),
        )
        def update_graph(xaxis, yaxis) -> go.Figure:
            if xaxis == None or yaxis == None:
                labels = dict(x="x", y="y")
                fig = px.scatter(x=[0], y=[0], labels=labels)
            else:
                prefilter_atnf = self.data[self.data["Catalog"] == "ATNF"]
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=prefilter_atnf[xaxis],
                        y=prefilter_atnf[yaxis],
                        mode="markers",
                        name="ATNF",
                        marker_line_color="black",
                        marker_line_width=0.5,
                        marker_size=4,
                    )
                )
                prefilter_fermi = self.data[self.data["Catalog"] != "ATNF"]
                fig.add_trace(
                    go.Scatter(
                        x=prefilter_fermi[xaxis],
                        y=prefilter_fermi[yaxis],
                        mode="markers",
                        name="Fermi",
                        marker_size=6,
                        marker_symbol="diamond",
                        marker_line_color="black",
                        marker_line_width=1,
                    )
                )
                fig.update_layout(
                    xaxis_title=to_label(xaxis, self.data_units[xaxis]),
                    yaxis_title=to_label(yaxis, self.data_units[yaxis]),
                )
            fig.update_layout(layout_plotly)
            return fig

        pio.templates.default = "plotly_dark"
        self.app.run_server(debug=debug, port=port)


# self.status_checklist = dash.html.Div(
#     [
#         dash.dcc.Checklist(
#             #         self.pihole_data.allStatuses(),
#             #         self.pihole_data.allStatuses(),
#             inline=True,
#             className="checklist",
#             id="status-check",
#         ),
#         dash.html.Span(
#             [
#                 "Query status",
#             ]
#         ),
#     ]
# )

# self.catalog_checklist = dash.html.Div(
#     [
#         dash.dcc.Checklist(
#             psr_catalogs,
#             psr_catalogs,
#             inline=True,
#             className="checklist",
#             id="catalog-check",
#         ),
#         dash.html.Span(
#             [
#                 "Pulsar catalogs",
#             ]
#         ),
#     ],
#     id="catalog-checklist",
# )

# self.client_dropdown = dash.html.Div([
#     dash.html.Span([
#         "Clients",
#     ]),
#     dash.dcc.Dropdown(
#         self.pihole_data.allClients(),
#         self.pihole_data.allClients(),
#         multi=True, searchable=False,
#         placeholder="Select clients",
#         id="client-select"
#     )
# ], className="multi-dropdown")
# self.graph =


# @self.app.callback(
#             dash.Output("graph-tooltip", "show"),
#             dash.Output("graph-tooltip", "bbox"),
#             dash.Output("graph-tooltip", "children"),
#             dash.Input("graph-main", "hoverData"),
#         )
#         def display_hover(hoverData):
#             if hoverData is None:
#                 return False, dash.no_update, dash.no_update

#             # # demo only shows the first point, but other points may also be available
#             pt = hoverData["points"][0]
#             bbox = pt["bbox"]
#             # num = pt["pointNumber"]
#             take_data = self.data[
#                 ~((self.data["Catalog"] == "ATNF") ^ (pt["curveNumber"] == 0))
#             ]

#             # df_row = df.iloc[num]
#             # img_src = df_row["IMG_URL"]
#             # name = df_row["NAME"]
#             # form = df_row["FORM"]
#             # desc = df_row["DESC"]
#             # if len(desc) > 300:
#             #     desc = desc[:100] + "..."

#             # print (take_data.iloc[pt["pointNumber"]],)

#             pulsar = take_data.iloc[pt["pointNumber"]]

#             fig = go.Figure()
#             graph = dash.dcc.Graph(
#                 id="graph-sec",
#                 config={"displaylogo": False},
#                 figure=fig
#             )
#             fig.update_layout(
#                 xaxis=dict(type="log", exponentformat="power"),
#                 yaxis=dict(type="log", exponentformat="power")
#             )

#             children = [
#                 dash.html.Div(
#                     children=[*PulsarCard(pulsar), dash.html.Div(graph)],
#                     # style={"background-color": "black", "white-space": "normal"},
#                     className="hover-note",
#                 )
#             ]
#             return True, bbox, children
