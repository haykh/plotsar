import plotly.graph_objects as go


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

save_config = {
    "toImageButtonOptions": {
        "format": "png",
        "height": None,
        "width": None,
        "scale": 3,
    }
}

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

index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
