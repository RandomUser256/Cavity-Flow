import dash
from dash import dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import simulations

# ─── Equation registry ─────────────────────────────────────────────────────────
#
# Each entry:
#   label  – display name shown in the dropdown
#   group  – used to group options visually
#   run    – callable that returns a plotly Figure
#   params – list of parameter descriptors (id, label, default, min, max, step)
#   info   – placeholder text; user will fill this in later

EQUATIONS = {
    "1d_diffusion": {
        "label": "1D Diffusion Equation",
        "group": "1D Equations",
        "run": simulations.run_1d_diffusion,
        "params": [
            {"id": "nx",    "label": "Grid Points (nx)",     "default": 41,   "min": 10,    "max": 200,  "step": 1},
            {"id": "nt",    "label": "Time Steps (nt)",       "default": 20,   "min": 1,     "max": 500,  "step": 1},
            {"id": "nu",    "label": "Diffusion Coeff. (ν)", "default": 0.3,  "min": 0.01,  "max": 2.0,  "step": 0.01},
            {"id": "sigma", "label": "CFL Number (σ)",        "default": 0.2,  "min": 0.01,  "max": 0.49, "step": 0.01},
        ],
        "info": "Information about the 1D Diffusion Equation will be added here.",
    },
    "1d_linear_convection": {
        "label": "1D Linear Convection",
        "group": "1D Equations",
        "run": simulations.run_1d_linear_convection,
        "params": [
            {"id": "nx",    "label": "Grid Points (nx)",  "default": 41,  "min": 10,   "max": 200,  "step": 1},
            {"id": "nt",    "label": "Time Steps (nt)",    "default": 20,  "min": 1,    "max": 500,  "step": 1},
            {"id": "c",     "label": "Wave Speed (c)",     "default": 1.0, "min": 0.1,  "max": 5.0,  "step": 0.1},
            {"id": "sigma", "label": "CFL Number (σ)",     "default": 0.5, "min": 0.01, "max": 0.99, "step": 0.01},
        ],
        "info": "Information about the 1D Linear Convection Equation will be added here.",
    },
    "1d_nonlinear_convection": {
        "label": "1D Nonlinear Convection",
        "group": "1D Equations",
        "run": simulations.run_1d_nonlinear_convection,
        "params": [
            {"id": "nx", "label": "Grid Points (nx)", "default": 41,    "min": 10,    "max": 200, "step": 1},
            {"id": "nt", "label": "Time Steps (nt)",   "default": 20,    "min": 1,     "max": 500, "step": 1},
            {"id": "dt", "label": "Time Step (dt)",    "default": 0.025, "min": 0.001, "max": 0.1, "step": 0.001},
        ],
        "info": "Information about the 1D Nonlinear Convection Equation will be added here.",
    },
    "burgers_1d": {
        "label": "1D Burgers Equation",
        "group": "1D Equations",
        "run": simulations.run_burgers_1d,
        "params": [
            {"id": "nx", "label": "Grid Points (nx)", "default": 101,  "min": 10,   "max": 201, "step": 1},
            {"id": "nt", "label": "Time Steps (nt)",   "default": 100,  "min": 1,    "max": 500, "step": 1},
            {"id": "nu", "label": "Viscosity (ν)",     "default": 0.07, "min": 0.01, "max": 1.0, "step": 0.01},
        ],
        "info": "Information about the 1D Burgers Equation will be added here.",
    },
    "2d_laplace": {
        "label": "2D Laplace Equation",
        "group": "2D Equations",
        "run": simulations.run_2d_laplace,
        "params": [
            {"id": "nx",           "label": "Grid Points X (nx)",    "default": 31,   "min": 10,    "max": 80,   "step": 1},
            {"id": "ny",           "label": "Grid Points Y (ny)",    "default": 31,   "min": 10,    "max": 80,   "step": 1},
            {"id": "l1norm_target","label": "Convergence Tolerance", "default": 1e-4, "min": 1e-6,  "max": 1e-2, "step": 1e-5},
        ],
        "info": "Information about the 2D Laplace Equation will be added here.",
    },
    "2d_poisson": {
        "label": "2D Poisson Equation",
        "group": "2D Equations",
        "run": simulations.run_2d_poisson,
        "params": [
            {"id": "nx", "label": "Grid Points X (nx)", "default": 50,  "min": 10, "max": 100, "step": 1},
            {"id": "ny", "label": "Grid Points Y (ny)", "default": 50,  "min": 10, "max": 100, "step": 1},
            {"id": "nt", "label": "Iterations (nt)",    "default": 100, "min": 10, "max": 500, "step": 10},
        ],
        "info": "Information about the 2D Poisson Equation will be added here.",
    },
    "2d_diffusion": {
        "label": "2D Diffusion Equation",
        "group": "2D Equations",
        "run": simulations.run_2d_diffusion,
        "params": [
            {"id": "nx",    "label": "Grid Points X (nx)",     "default": 31,   "min": 10,    "max": 80,   "step": 1},
            {"id": "ny",    "label": "Grid Points Y (ny)",     "default": 31,   "min": 10,    "max": 80,   "step": 1},
            {"id": "nt",    "label": "Time Steps (nt)",         "default": 50,   "min": 1,     "max": 200,  "step": 1},
            {"id": "nu",    "label": "Diffusion Coeff. (ν)",   "default": 0.05, "min": 0.001, "max": 0.5,  "step": 0.001},
            {"id": "sigma", "label": "CFL Number (σ)",          "default": 0.25, "min": 0.01,  "max": 0.49, "step": 0.01},
        ],
        "info": "Information about the 2D Diffusion Equation will be added here.",
    },
    "2d_linear_convection": {
        "label": "2D Linear Convection",
        "group": "2D Equations",
        "run": simulations.run_2d_linear_convection,
        "params": [
            {"id": "nx",    "label": "Grid Points X (nx)", "default": 81,  "min": 10,   "max": 150,  "step": 1},
            {"id": "ny",    "label": "Grid Points Y (ny)", "default": 81,  "min": 10,   "max": 150,  "step": 1},
            {"id": "nt",    "label": "Time Steps (nt)",     "default": 100, "min": 1,    "max": 300,  "step": 1},
            {"id": "c",     "label": "Wave Speed (c)",      "default": 1.0, "min": 0.1,  "max": 5.0,  "step": 0.1},
            {"id": "sigma", "label": "CFL Number (σ)",      "default": 0.2, "min": 0.01, "max": 0.49, "step": 0.01},
        ],
        "info": "Information about the 2D Linear Convection Equation will be added here.",
    },
    "2d_nonlinear_convection": {
        "label": "2D Nonlinear Convection",
        "group": "2D Equations",
        "run": simulations.run_2d_nonlinear_convection,
        "params": [
            {"id": "nx",    "label": "Grid Points X (nx)", "default": 101, "min": 10,   "max": 150,  "step": 1},
            {"id": "ny",    "label": "Grid Points Y (ny)", "default": 101, "min": 10,   "max": 150,  "step": 1},
            {"id": "nt",    "label": "Time Steps (nt)",     "default": 80,  "min": 1,    "max": 300,  "step": 1},
            {"id": "sigma", "label": "CFL Number (σ)",      "default": 0.2, "min": 0.01, "max": 0.49, "step": 0.01},
        ],
        "info": "Information about the 2D Nonlinear Convection Equation will be added here.",
    },
    "burgers_2d": {
        "label": "2D Burgers Equation",
        "group": "2D Equations",
        "run": simulations.run_burgers_2d,
        "params": [
            {"id": "nx",    "label": "Grid Points X (nx)", "default": 41,    "min": 10,     "max": 80,   "step": 1},
            {"id": "ny",    "label": "Grid Points Y (ny)", "default": 41,    "min": 10,     "max": 80,   "step": 1},
            {"id": "nt",    "label": "Time Steps (nt)",     "default": 120,   "min": 1,      "max": 300,  "step": 1},
            {"id": "nu",    "label": "Viscosity (ν)",       "default": 0.01,  "min": 0.001,  "max": 0.5,  "step": 0.001},
            {"id": "sigma", "label": "CFL Number (σ)",      "default": 0.0009,"min": 0.0001, "max": 0.01, "step": 0.0001},
        ],
        "info": "Information about the 2D Burgers Equation will be added here.",
    },
    "cavity_flow": {
        "label": "Cavity Flow (Navier-Stokes)",
        "group": "Navier-Stokes",
        "run": simulations.run_cavity_flow,
        "params": [
            {"id": "nx",  "label": "Grid Points X (nx)",         "default": 41,    "min": 10,    "max": 61,    "step": 1},
            {"id": "ny",  "label": "Grid Points Y (ny)",         "default": 41,    "min": 10,    "max": 61,    "step": 1},
            {"id": "nt",  "label": "Time Steps (nt)",             "default": 500,   "min": 50,    "max": 1000,  "step": 50},
            {"id": "nit", "label": "Pressure Iterations (nit)",  "default": 50,    "min": 10,    "max": 100,   "step": 5},
            {"id": "rho", "label": "Density (ρ)",                "default": 1.0,   "min": 0.1,   "max": 10.0,  "step": 0.1},
            {"id": "nu",  "label": "Kinematic Viscosity (ν)",    "default": 0.1,   "min": 0.01,  "max": 1.0,   "step": 0.01},
            {"id": "dt",  "label": "Time Step (dt)",             "default": 0.001, "min": 0.0001,"max": 0.01,  "step": 0.0001},
        ],
        "info": "Information about the Cavity Flow Navier-Stokes simulation will be added here.",
    },
    "channel_flow": {
        "label": "Channel Flow (Navier-Stokes)",
        "group": "Navier-Stokes",
        "run": simulations.run_channel_flow,
        "params": [
            {"id": "nx",        "label": "Grid Points X (nx)",        "default": 41,   "min": 10,    "max": 61,   "step": 1},
            {"id": "ny",        "label": "Grid Points Y (ny)",        "default": 41,   "min": 10,    "max": 61,   "step": 1},
            {"id": "nit",       "label": "Pressure Iterations (nit)", "default": 50,   "min": 10,    "max": 100,  "step": 5},
            {"id": "rho",       "label": "Density (ρ)",               "default": 1.0,  "min": 0.1,   "max": 10.0, "step": 0.1},
            {"id": "nu",        "label": "Kinematic Viscosity (ν)",   "default": 0.1,  "min": 0.01,  "max": 1.0,  "step": 0.01},
            {"id": "F",         "label": "Body Force (F)",            "default": 1.0,  "min": 0.1,   "max": 5.0,  "step": 0.1},
            {"id": "dt",        "label": "Time Step (dt)",            "default": 0.01, "min": 0.001, "max": 0.1,  "step": 0.001},
            {"id": "max_steps", "label": "Max Iterations",            "default": 500,  "min": 50,    "max": 2000, "step": 50},
        ],
        "info": "Information about the Channel Flow Navier-Stokes simulation will be added here.",
    },
}


# ─── Welcome figure ────────────────────────────────────────────────────────────

def _welcome_figure():
    fig = go.Figure()
    fig.update_layout(
        template="plotly_dark",
        height=520,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[dict(
            text="Select an equation and click  <b>Run Simulation</b>  to begin",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=18, color="#888"),
            align="center",
        )],
    )
    return fig


# ─── App ───────────────────────────────────────────────────────────────────────

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    title="CFD Equation Explorer",
)

# Build grouped dropdown options
_groups: dict = {}
for key, cfg in EQUATIONS.items():
    _groups.setdefault(cfg["group"], []).append({"label": cfg["label"], "value": key})

dropdown_options = [
    {"label": html.Span(g, style={"fontWeight": "bold", "color": "#aaa"}), "value": f"__group_{g}__", "disabled": True}
    for g in _groups
    for _ in [None]  # type: ignore — just to interleave
]
# Rebuild as flat list with group headers
flat_options = []
for group, items in _groups.items():
    flat_options.append({"label": f"── {group} ──", "value": f"__group_{group}__", "disabled": True})
    flat_options.extend(items)

# ─── Sidebar ───────────────────────────────────────────────────────────────────

sidebar = html.Div(
    [
        # Title
        html.Div(
            html.H4("CFD Explorer", className="mb-0 fw-bold",
                    style={"color": "#4fc3f7", "letterSpacing": "0.05em"}),
            className="mb-4",
        ),

        # Equation selector
        html.Label("Equation", className="text-secondary small fw-bold text-uppercase mb-1"),
        dcc.Dropdown(
            id="equation-selector",
            options=flat_options,
            value="1d_diffusion",
            clearable=False,
            style={"color": "#222"},
        ),

        html.Hr(style={"borderColor": "#444", "margin": "1.2rem 0"}),

        # Parameters (populated by callback)
        html.Label("Parameters", className="text-secondary small fw-bold text-uppercase mb-2"),
        html.Div(id="params-container"),

        html.Hr(style={"borderColor": "#444", "margin": "1.2rem 0"}),

        # Run button
        dbc.Button(
            [html.I(className="me-2"), "Run Simulation"],
            id="run-btn",
            color="primary",
            className="w-100",
            style={"fontWeight": "600"},
        ),

        # Hidden store for parameter names of current equation
        dcc.Store(id="param-names-store"),
    ],
    style={
        "position": "sticky",
        "top": 0,
        "height": "100vh",
        "overflowY": "auto",
        "background": "#1a1a2e",
        "padding": "1.5rem 1.2rem",
        "borderRight": "1px solid #2d2d4a",
    },
)

# ─── Main content ──────────────────────────────────────────────────────────────

main_content = html.Div(
    [
        # Page heading
        html.Div(
            [
                html.H2("CFD Equation Explorer", className="fw-bold mb-1",
                        style={"color": "#e0e0e0"}),
                html.P(
                    "Numerical methods for computational fluid dynamics — "
                    "select an equation, adjust its parameters, and run the simulation.",
                    className="text-secondary mb-0",
                    style={"fontSize": "0.95rem"},
                ),
            ],
            className="mb-4",
        ),

        # Simulation output (graph + loading spinner)
        dcc.Loading(
            id="loading-graph",
            type="circle",
            color="#4fc3f7",
            children=dcc.Graph(
                id="sim-graph",
                figure=_welcome_figure(),
                config={"displayModeBar": True, "scrollZoom": True},
            ),
        ),

        # Status line
        html.Div(id="sim-status", className="text-secondary mt-2",
                 style={"fontSize": "0.82rem", "minHeight": "1.2rem"}),

        html.Hr(style={"borderColor": "#2d2d4a", "margin": "1.5rem 0"}),

        # About / info section
        html.Label("About this Equation",
                   className="text-secondary small fw-bold text-uppercase mb-2"),
        dbc.Card(
            dbc.CardBody(
                html.P(id="info-text",
                       className="mb-0",
                       style={"color": "#aaa", "fontSize": "0.92rem", "whiteSpace": "pre-wrap"}),
            ),
            style={"background": "#1a1a2e", "border": "1px solid #2d2d4a"},
        ),
    ],
    style={
        "background": "#16213e",
        "minHeight": "100vh",
        "padding": "2rem 2rem 3rem",
    },
)

# ─── Layout ────────────────────────────────────────────────────────────────────

app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(sidebar, width=3, className="p-0"),
            dbc.Col(main_content, width=9),
        ],
        className="g-0",
    ),
    fluid=True,
    style={"background": "#16213e", "padding": 0},
)


# ─── Callbacks ─────────────────────────────────────────────────────────────────

@app.callback(
    Output("params-container", "children"),
    Output("param-names-store", "data"),
    Output("info-text", "children"),
    Input("equation-selector", "value"),
)
def update_controls(equation):
    """Rebuild the parameter inputs and info text whenever a new equation is selected."""
    if not equation or equation.startswith("__group_"):
        return [], [], ""

    cfg = EQUATIONS.get(equation)
    if cfg is None:
        return [], [], ""

    rows = []
    names = []
    for i, p in enumerate(cfg["params"]):
        rows.append(
            html.Div(
                [
                    html.Label(
                        p["label"],
                        className="text-secondary mb-1",
                        style={"fontSize": "0.82rem"},
                    ),
                    dbc.Input(
                        id={"type": "param-input", "index": i},
                        type="number",
                        value=p["default"],
                        min=p["min"],
                        max=p["max"],
                        step=p["step"],
                        debounce=True,
                        className="mb-2",
                        style={"fontSize": "0.88rem"},
                    ),
                ]
            )
        )
        names.append(p["id"])

    return rows, names, cfg["info"]


@app.callback(
    Output("sim-graph", "figure"),
    Output("sim-status", "children"),
    Input("run-btn", "n_clicks"),
    State("equation-selector", "value"),
    State({"type": "param-input", "index": ALL}, "value"),
    State("param-names-store", "data"),
    prevent_initial_call=True,
)
def run_simulation(n_clicks, equation, param_values, param_names):
    """Collect parameter values, run the selected simulation, and return the Plotly figure."""
    if not equation or equation.startswith("__group_"):
        raise dash.exceptions.PreventUpdate

    # Build kwargs dict, replacing None with the default from the config
    cfg = EQUATIONS[equation]
    params = {}
    for name, val, p_def in zip(param_names or [], param_values or [], cfg["params"]):
        params[name] = val if val is not None else p_def["default"]

    try:
        fig = cfg["run"](**params)
        param_summary = "  |  ".join(f"{k} = {v}" for k, v in params.items())
        return fig, f"Done — {param_summary}"
    except Exception as exc:
        err_fig = go.Figure()
        err_fig.update_layout(
            template="plotly_dark",
            height=520,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(
                text=f"<b>Simulation error</b><br>{exc}",
                xref="paper", yref="paper", x=0.5, y=0.5,
                showarrow=False, font=dict(size=14, color="#ef5350"),
                align="center",
            )],
        )
        return err_fig, f"Error: {exc}"


# ─── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
