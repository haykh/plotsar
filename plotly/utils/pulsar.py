import dash
import dash_latex as dl
import numpy as np
import plotly

from .defs import *
from .configs import *


def PulsarCard(pulsar):
    if pulsar["P0"] < 0.1:
        period = rf"$P = {{{exp_tex(pulsar['P0'] * 1000)}}}~\textrm{{ms}}$"
    else:
        period = rf"$P = {{{exp_tex(pulsar['P0'])}}}~\textrm{{s}}$"
    pdot = rf"$\dot{{P}} = {{{exp_tex(pulsar['P1'])}}}$"
    rlc = rf"$R_{{\rm LC}} = {{{exp_tex(pulsar['RLC'])}}}~\textrm{{km}}$"
    bstar = rf"$B_* = {{{exp_tex(pulsar['Bsurf'])}}}~\textrm{{G}}$"
    edot = rf"$\dot{{E}} = {{{exp_tex(pulsar['Edot'])}}}~\textrm{{erg/s}}$"
    if pulsar["Catalog"] == "ATNF":
        spectrum = None
    else:
        xedges = np.sort(np.unique(pulsar["Band"])) / 1e3
        xc, yc = np.sqrt(xedges[:-1] * xedges[1:]), pulsar["nuFnu_Band"]
        xs, ys = (
            np.array(pulsar["Band"]).flatten() / 1e3,
            np.reshape(
                [pulsar["nuFnu_Band"] * 2], (2, len(pulsar["nuFnu_Band"]))
            ).T.flatten(),
        )
        yerr_up = (
            np.array(pulsar["nuFnu_Band"])
            * np.array([x[1] for x in pulsar["Unc_Flux_Band"]])
            / np.array(pulsar["Flux_Band"])
        )
        yerr_dwn = (
            np.array(pulsar["nuFnu_Band"])
            * np.array([np.abs(x[0]) for x in pulsar["Unc_Flux_Band"]])
            / np.array(pulsar["Flux_Band"])
        )
        ymax = np.ceil(np.log10(ys.max()))
        ymin = ymax - 4
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=xs, y=ys, mode="lines", line_color=plotly.colors.DEFAULT_PLOTLY_COLORS[1]
            )
        )
        fig.add_trace(
            go.Scatter(
                x=xc,
                y=yc,
                marker_color=plotly.colors.DEFAULT_PLOTLY_COLORS[1],
                mode="markers",
                error_y=dict(
                    type="data",
                    symmetric=False,
                    array=yerr_up,
                    arrayminus=np.nan_to_num(yerr_dwn, nan=1),
                ),
            )
        )
        fig.update_layout(
            layout_plotly,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            xaxis_title="energy [GeV]",
            yaxis_title="flux density [erg/s/cm^2]",
            xaxis_range=[np.log10(xedges[0]), np.log10(xedges[-1])],
            yaxis_range=[ymin, ymax],
        )
        spectrum = dash.dcc.Graph(
            figure=fig, id="spectrum", config={"displaylogo": False}
        )
    return [
        dash.html.H1(pulsar["Name"]),
        dl.DashLatex(period),
        dash.html.Br(),
        dl.DashLatex(pdot),
        dash.html.Br(),
        dl.DashLatex(bstar),
        dash.html.Br(),
        dl.DashLatex(edot),
        dash.html.Br(),
        dl.DashLatex(rlc),
        dash.html.Br(),
        dash.html.Div([spectrum], id="psr-spectrum"),
    ]
