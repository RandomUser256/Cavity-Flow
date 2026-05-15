"""
Block-based content system for the CFD Explorer info panels.

Block constructors return plain dicts; render_blocks() converts them to Dash components.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


# ─── Block constructors ────────────────────────────────────────────────────────

def collapsible(title, *children):
    """Expanding/collapsing section that can contain any other blocks."""
    return {"type": "collapsible", "title": title, "children": list(children)}


def latex(expr):
    """Display-mode LaTeX equation rendered via MathJax."""
    return {"type": "latex", "expr": expr}


def image_text(src, caption, img_side="left"):
    """Side-by-side image and text. img_side: 'left' or 'right'."""
    return {"type": "image_text", "src": src, "caption": caption, "img_side": img_side}


def bullets(*items):
    """Bullet list of strings."""
    return {"type": "bullets", "items": list(items)}


def paragraph(content):
    """Plain text paragraph."""
    return {"type": "text", "content": content}


# ─── Renderer ──────────────────────────────────────────────────────────────────

_TEXT_STYLE = {"color": "#bbb", "fontSize": "0.92rem", "lineHeight": "1.6"}


def render_blocks(blocks):
    """Convert a list of block descriptors into Dash components."""
    components = []
    for block in blocks:
        btype = block["type"]

        if btype == "text":
            components.append(
                html.P(block["content"], style={**_TEXT_STYLE, "margin": "0 0 0.6rem"})
            )

        elif btype == "latex":
            components.append(
                dcc.Markdown(
                    f"$$\n{block['expr']}\n$$",
                    mathjax=True,
                    style={"overflowX": "auto", "margin": "0.5rem 0", "textAlign": "center"},
                )
            )

        elif btype == "bullets":
            components.append(
                html.Ul(
                    [html.Li(item, style=_TEXT_STYLE) for item in block["items"]],
                    style={"paddingLeft": "1.4rem", "margin": "0.4rem 0 0.8rem"},
                )
            )

        elif btype == "image_text":
            img_col = dbc.Col(
                html.Img(
                    src=block["src"],
                    style={"width": "100%", "borderRadius": "6px",
                           "border": "1px solid #2d2d4a"},
                ),
                width=5,
            )
            txt_col = dbc.Col(html.P(block["caption"], style=_TEXT_STYLE), width=7)
            cols = (
                [img_col, txt_col]
                if block.get("img_side", "left") == "left"
                else [txt_col, img_col]
            )
            components.append(dbc.Row(cols, className="align-items-center mb-3"))

        elif btype == "collapsible":
            components.append(
                dbc.Accordion(
                    dbc.AccordionItem(
                        html.Div(
                            render_blocks(block["children"]),
                            style={"padding": "0.25rem 0"},
                        ),
                        title=block["title"],
                    ),
                    start_collapsed=True,
                    className="mb-2",
                )
            )

    return components


# ─── General / home page content ──────────────────────────────────────────────

HOME_CONTENT = [
    paragraph(
        "This interactive tool explores the numerical methods used in Computational Fluid Dynamics (CFD). "
        "Starting from simple 1D transport equations and building up to the full Navier-Stokes equations, "
        "each simulation lets you adjust physical parameters and observe the results in real time."
    ),
    collapsible(
        "What is Computational Fluid Dynamics?",
        paragraph(
            "CFD uses numerical algorithms to solve the governing equations of fluid motion. "
            "Real-world flows rarely admit analytical solutions, so we discretize the equations "
            "onto a mesh and solve the resulting algebraic system at each time step."
        ),
        bullets(
            "Replace continuous derivatives with finite differences on a regular grid",
            "March the solution forward in time (explicit) or solve a coupled system (implicit)",
            "Visualize scalar fields (pressure, temperature) and vector fields (velocity)",
        ),
    ),
    collapsible(
        "Finite Difference Method (FDM)",
        paragraph(
            "All solvers here use the Finite Difference Method: derivatives are approximated "
            "using the values at neighboring grid points."
        ),
        paragraph("First-order backward difference (upwind for convection):"),
        latex(r"\frac{\partial u}{\partial x} \approx \frac{u_i - u_{i-1}}{\Delta x}"),
        paragraph("Second-order centered difference for the Laplacian:"),
        latex(r"\frac{\partial^2 u}{\partial x^2} \approx \frac{u_{i+1} - 2u_i + u_{i-1}}{\Delta x^2}"),
    ),
    collapsible(
        "Numerical Stability — CFL Condition",
        paragraph(
            "Explicit time-stepping imposes a maximum allowable time step to remain stable. "
            "The Courant-Friedrichs-Lewy (CFL) condition for convection problems:"
        ),
        latex(r"\sigma = \frac{c \,\Delta t}{\Delta x} \leq 1"),
        paragraph("For diffusion the stability constraint is:"),
        latex(r"\nu \frac{\Delta t}{\Delta x^2} \leq \frac{1}{2}"),
        paragraph("Exceeding these limits causes the numerical solution to grow without bound."),
    ),
    collapsible(
        "Equation Progression",
        paragraph("Equations are ordered from simple to complex:"),
        bullets(
            "1D Linear Convection — constant-speed transport of a wave profile",
            "1D Nonlinear Convection — self-steepening due to velocity-dependent wave speed",
            "1D Diffusion — heat-equation spreading with finite viscosity",
            "1D Burgers — combines nonlinear convection and diffusion",
            "2D Laplace / Poisson — steady-state elliptic problems",
            "2D extensions of diffusion and convection",
            "Navier-Stokes: lid-driven Cavity Flow and pressure-driven Channel Flow",
        ),
    ),
    collapsible(
        "Navier-Stokes Equations",
        paragraph(
            "The incompressible Navier-Stokes equations govern real viscous fluid flows. "
            "They express conservation of momentum and mass:"
        ),
        latex(
            r"\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} "
            r"= -\frac{1}{\rho}\nabla p + \nu \nabla^2 \mathbf{u}"
        ),
        latex(r"\nabla \cdot \mathbf{u} = 0"),
        paragraph(
            "Pressure is determined implicitly through a Poisson equation derived from the "
            "incompressibility constraint, solved iteratively at every time step."
        ),
    ),
]


# ─── Per-equation info blocks ──────────────────────────────────────────────────

INFO_1D_DIFFUSION = [
    paragraph(
        "The 1D diffusion equation (heat equation) models how a scalar quantity — "
        "temperature, concentration, or vorticity — spreads through a medium due to molecular diffusion."
    ),
    latex(r"\frac{\partial u}{\partial t} = \nu \frac{\partial^2 u}{\partial x^2}"),
    collapsible(
        "Finite Difference Scheme",
        paragraph("Forward-Time, Centered-Space (FTCS) discretization:"),
        latex(
            r"u_i^{n+1} = u_i^n + \nu \frac{\Delta t}{\Delta x^2}"
            r"\left(u_{i+1}^n - 2u_i^n + u_{i-1}^n\right)"
        ),
        paragraph("First-order in time, second-order in space."),
    ),
    collapsible(
        "Stability",
        paragraph("FTCS is conditionally stable; the requirement is:"),
        latex(r"\nu \frac{\Delta t}{\Delta x^2} \leq \frac{1}{2}"),
        paragraph("The CFL parameter σ directly controls this ratio — keep it ≤ 0.49."),
    ),
    collapsible(
        "Parameters",
        bullets(
            "nx — spatial grid resolution (more points → smoother solution)",
            "nt — number of time steps (higher → further evolved in time)",
            "ν — diffusion coefficient (larger → faster spreading)",
            "σ — stability parameter; must stay ≤ 0.49",
        ),
    ),
]

INFO_1D_LINEAR_CONVECTION = [
    paragraph(
        "The 1D linear convection equation describes the transport of a wave profile at a "
        "constant speed c without change in shape (in the continuous, exact case)."
    ),
    latex(r"\frac{\partial u}{\partial t} + c \frac{\partial u}{\partial x} = 0"),
    collapsible(
        "Finite Difference Scheme",
        paragraph("First-order upwind (backward in space, forward in time):"),
        latex(r"u_i^{n+1} = u_i^n - c \frac{\Delta t}{\Delta x}\left(u_i^n - u_{i-1}^n\right)"),
        paragraph(
            "The backward difference is chosen in the direction of wave propagation "
            "to ensure numerical stability."
        ),
    ),
    collapsible(
        "Stability — CFL Condition",
        paragraph("The scheme is stable when:"),
        latex(r"\sigma = \frac{c \,\Delta t}{\Delta x} \leq 1"),
        paragraph("At σ = 1 the upwind scheme is exact (zero numerical diffusion)."),
    ),
    collapsible(
        "Parameters",
        bullets(
            "nx — number of spatial grid points",
            "nt — number of time steps",
            "c — wave propagation speed",
            "σ — CFL number; must be ≤ 1 for stability",
        ),
    ),
]

INFO_1D_NONLINEAR_CONVECTION = [
    paragraph(
        "The nonlinear convection equation is like the linear case but the wave speed equals the "
        "solution itself. Faster parts of the wave overtake slower parts, steepening the profile "
        "into a shock."
    ),
    latex(r"\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} = 0"),
    collapsible(
        "Finite Difference Scheme",
        paragraph("First-order upwind discretization with velocity-dependent speed:"),
        latex(
            r"u_i^{n+1} = u_i^n - u_i^n \frac{\Delta t}{\Delta x}"
            r"\left(u_i^n - u_{i-1}^n\right)"
        ),
    ),
    collapsible(
        "Parameters",
        bullets(
            "nx — number of spatial grid points",
            "nt — number of time steps",
            "dt — time step size Δt; keep small to avoid instability",
        ),
    ),
]

INFO_BURGERS_1D = [
    paragraph(
        "Modelo de movimiento turbulento de fluidos propuesto por J.M Burgers, siendo publicados todos sus artículos respecto al modelo en 1948 (Beck, 1948). "
        "La ecuación de Burgers combina la convección no lineal con la difusión viscosa."
    ),
    collapsible(
        "Solución exacta",
        paragraph(
            "The Cole-Hopf transformation linearizes Burgers' equation. "
            "The analytical solution is computed with SymPy and shown alongside the numerical result."
        ),
        latex(r"u(x,t) = -2\nu \frac{\partial}{\partial x} \ln \phi(x,t)"),
    ),
    collapsible(
        "Interpretación física",
        bullets(
            "La convección de la curva representa dispersión de la energía cinética del fluido.",
            "Una mayor difusión suaviza la dispersión de la energía.",
            "Mayor viscosidad -> una difusión más suave. Menor viscosidad -> cambios bruscos en la ecuación.",
        ),
    ),
    collapsible(
        "Parámetros",
        bullets(
            "nx, ny - Cantidad de puntos a representar en los ejes (x,y) respectivamente",
            "nt - Cantidad de unidades de tiempo consideradas en el desplazamiento de la ecuación",
            "ν (viscosidad cinemática) - Esta controla la fuerza de dispersión de la ecuación",
        ),
    ),
    collapsible(
        "Usos/aplicaciones de la ecuación",
        bullets(
            "Simplificación de la ecuación Navier-Stokes.",
            "Modelo de referencia para analizar otras Ecuaciones Diferenciales Parciales.",
            "Caracterización de otras leyes de conservación escalares viscosas.",
        )
    ),
    collapsible(
        "Referencias",
        bullets(
             "Beck, M. (s.f.). Burgers Equation. Herit-Watt University. https://math.bu.edu/people/mabeck/Beck2012_burgers.pdf"
        )
    )
]

INFO_2D_LAPLACE = [
    paragraph(
        "The 2D Laplace equation governs steady-state diffusion: temperature at equilibrium, "
        "electrostatic potential in free space, or the velocity potential of inviscid irrotational flow."
    ),
    latex(r"\frac{\partial^2 p}{\partial x^2} + \frac{\partial^2 p}{\partial y^2} = 0"),
    collapsible(
        "Iterative Solver",
        paragraph(
            "With no time dependence, the equation is solved by repeated Jacobi iteration "
            "until the L1 norm of successive differences falls below the tolerance:"
        ),
        latex(
            r"p_{i,j} = \frac{(p_{i+1,j} + p_{i-1,j})\Delta y^2 "
            r"+ (p_{i,j+1} + p_{i,j-1})\Delta x^2}{2(\Delta x^2 + \Delta y^2)}"
        ),
    ),
    collapsible(
        "Boundary Conditions",
        bullets(
            "p = 0 on the top and bottom edges",
            "p = y on the right edge (linear gradient)",
            "∂p/∂x = 0 on the left edge (zero-flux Neumann condition)",
        ),
    ),
    collapsible(
        "Parameters",
        bullets(
            "nx — grid points in x",
            "ny — grid points in y",
            "Convergence Tolerance — L1-norm threshold for stopping iteration",
        ),
    ),
]

INFO_2D_POISSON = [
    paragraph(
        "The Poisson equation is the Laplace equation with a non-zero source term. "
        "It appears in electrostatics, heat conduction with sources, and as the "
        "pressure equation in incompressible flow solvers."
    ),
    latex(r"\frac{\partial^2 p}{\partial x^2} + \frac{\partial^2 p}{\partial y^2} = b(x,y)"),
    collapsible(
        "Source Term",
        paragraph(
            "The source term b is two point sources of equal and opposite strength "
            "placed symmetrically inside the domain:"
        ),
        latex(
            r"b_{i,j} = \begin{cases}"
            r"+100 & \text{near } (x, y) = (0.25L_x,\, 0.25L_y) \\"
            r"-100 & \text{near } (x, y) = (0.75L_x,\, 0.75L_y)"
            r"\end{cases}"
        ),
    ),
    collapsible(
        "Finite Difference Scheme",
        paragraph("Iterative update at each interior grid point:"),
        latex(
            r"p_{i,j}^{n+1} = \frac{(p_{i+1,j}^n + p_{i-1,j}^n)\Delta y^2 "
            r"+ (p_{i,j+1}^n + p_{i,j-1}^n)\Delta x^2 - b_{i,j}\Delta x^2\Delta y^2}"
            r"{2(\Delta x^2 + \Delta y^2)}"
        ),
    ),
    collapsible(
        "Parameters",
        bullets(
            "nx — grid points in x",
            "ny — grid points in y",
            "nt — iteration count (more → closer to converged solution)",
        ),
    ),
]

INFO_2D_DIFFUSION = [
    paragraph(
        "The 2D diffusion equation extends the 1D heat equation to two spatial dimensions. "
        "An initial square pulse spreads radially outward over time."
    ),
    latex(
        r"\frac{\partial u}{\partial t} = \nu \left("
        r"\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right)"
    ),
    collapsible(
        "Finite Difference Scheme",
        paragraph("Explicit FTCS extended to 2D:"),
        latex(
            r"u_{i,j}^{n+1} = u_{i,j}^n + \nu\Delta t\left("
            r"\frac{u_{i+1,j} - 2u_{i,j} + u_{i-1,j}}{\Delta x^2} + "
            r"\frac{u_{i,j+1} - 2u_{i,j} + u_{i,j-1}}{\Delta y^2}\right)"
        ),
    ),
    collapsible(
        "Stability",
        paragraph("The 2D stability condition is:"),
        latex(
            r"\nu\Delta t\left(\frac{1}{\Delta x^2} + \frac{1}{\Delta y^2}\right) \leq \frac{1}{2}"
        ),
    ),
    collapsible(
        "Parameters",
        bullets(
            "nx, ny — grid dimensions",
            "nt — time steps",
            "ν — diffusion coefficient",
            "σ — CFL-like stability parameter; keep ≤ 0.49",
        ),
    ),
]

INFO_2D_LINEAR_CONVECTION = [
    paragraph(
        "The 2D linear convection equation transports a scalar field at constant velocity (c, c) "
        "in both the x and y directions simultaneously."
    ),
    latex(
        r"\frac{\partial u}{\partial t} "
        r"+ c\frac{\partial u}{\partial x} + c\frac{\partial u}{\partial y} = 0"
    ),
    collapsible(
        "Finite Difference Scheme",
        paragraph("First-order upwind in both spatial directions:"),
        latex(
            r"u_{i,j}^{n+1} = u_{i,j}^n "
            r"- c\frac{\Delta t}{\Delta x}(u_{i,j}^n - u_{i-1,j}^n) "
            r"- c\frac{\Delta t}{\Delta y}(u_{i,j}^n - u_{i,j-1}^n)"
        ),
    ),
    collapsible(
        "Parameters",
        bullets(
            "nx, ny — grid dimensions",
            "nt — time steps",
            "c — wave speed in both directions",
            "σ — CFL number; must be ≤ 1",
        ),
    ),
]

INFO_2D_NONLINEAR_CONVECTION = [
    paragraph(
        "The 2D nonlinear convection equation extends the 1D case to two velocity components "
        "u and v that each advect themselves and are coupled through the other."
    ),
    latex(
        r"\frac{\partial u}{\partial t} "
        r"+ u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} = 0"
    ),
    latex(
        r"\frac{\partial v}{\partial t} "
        r"+ u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y} = 0"
    ),
    collapsible(
        "Visualization",
        paragraph(
            "Output shows the u and v components as side-by-side surface plots, "
            "so you can compare how steepening develops differently in each direction."
        ),
    ),
    collapsible(
        "Parameters",
        bullets(
            "nx, ny — grid dimensions",
            "nt — time steps",
            "σ — CFL number",
        ),
    ),
]

INFO_BURGERS_2D = [
    paragraph(
        "La ecuación de Burger 2D incorpora la difusión viscosa a la convección no lineal en 2D."
        "Both velocity components are evolved simultaneously under the same PDE structure."
    ),
    latex(
        r"\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} "
        r"= \nu\left(\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right)"
    ),
    latex(
        r"\frac{\partial v}{\partial t} + u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y} "
        r"= \nu\left(\frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2}\right)"
    ),
    paragraph(
        "La ecuación anterior se discretiza para ser aproximada. Su forma resultante es la siguiente: "
    ),
    latex(
        r"\begin{split}& \frac{u_{i,j}^{n+1} - u_{i,j}^n}{\Delta t} + u_{i,j}^n \frac{u_{i,j}^n-u_{i-1,j}^n}{\Delta x} + v_{i,j}^n \frac{u_{i,j}^n - u_{i,j-1}^n}{\Delta y} = \\& \qquad \nu \left( \frac{u_{i+1,j}^n - 2u_{i,j}^n+u_{i-1,j}^n}{\Delta x^2} + \frac{u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2} \right)\end{split}"
    ),
    latex(
        r"\begin{split} v_{i,j}^{n+1} = & v_{i,j}^n - \frac{\Delta t}{\Delta x} u_{i,j}^n (v_{i,j}^n - v_{i-1,j}^n) - \frac{\Delta t}{\Delta y} v_{i,j}^n (v_{i,j}^n - v_{i,j-1}^n) \\& + \frac{\nu \Delta t}{\Delta x^2}(v_{i+1,j}^n-2v_{i,j}^n+v_{i-1,j}^n) + \frac{\nu \Delta t}{\Delta y^2} (v_{i,j+1}^n - 2v_{i,j}^n + v_{i,j-1}^n)\end{split}"
    ),
    collapsible(
        "Interpretación física",
        paragraph("Two competing effects shape the solution:"),
        bullets(
            "La convección de la curva representa dispersión de la energía cinética del fluido.",
            "Una mayor difusión suaviza la dispersión de la energía.",
            "Mayor viscosidad -> una difusión más suave. Menor viscosidad -> cambios bruscos en la ecuación.",
        ),
    ),
    collapsible(
        "Parámetros",
        bullets(
            "nx, ny - Cantidad de puntos a representar en los ejes (x,y) respectivamente",
            "nt - Cantidad de unidades de tiempo consideradas en el desplazamiento de la ecuación",
            "ν (viscosidad cinemática) - Esta controla la fuerza de dispersión de la ecuación",
            "σ — parámetro de estabilidad (recomendado usar valores pequeños)",
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
             "Beck, M. (s.f.). Burgers Equation. Herit-Watt University. https://math.bu.edu/people/mabeck/Beck2012_burgers.pdf"
        )
    )
]

INFO_CAVITY_FLOW = [
    paragraph(
        "El problema “Lid-Driven Cavity” plantea un contenedor cuadrado, delimitado a dos dimensiones y con su tapa o pared superior sometido a movimiento"
        " Ha sido ampliamente estudiado en el ámbito de mecánica de fluidos y se han propuesto numerosas soluciones diversas, entre las cuales están las ecuaciones Navier-Stokes."
    ),
    collapsible(
        "Ecuaciones fundamentales",
        paragraph("Momento u (eje x):"),
        latex(
            r"\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} "
            r"= -\frac{1}{\rho}\frac{\partial p}{\partial x} "
            r"+ \nu\left(\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right)"
        ),
        paragraph("Momento v (eje y):"),
        latex(
            r"\frac{\partial v}{\partial t} + u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y} "
            r"= -\frac{1}{\rho}\frac{\partial p}{\partial y} "
            r"+ \nu\left(\frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2}\right)"
        ),
        paragraph("Ecuación de presión Poisson (derivado de la ecuación de incompresibilidad):"),
        latex(
            r"\frac{\partial^2 p}{\partial x^2}+\frac{\partial^2 p}{\partial y^2} = -\rho\left(\frac{\partial u}{\partial x}\frac{\partial u}{\partial x}+2\frac{\partial u}{\partial y}\frac{\partial v}{\partial x}+\frac{\partial v}{\partial y}\frac{\partial v}{\partial y} \right)"

        ),
    ),
    collapsible(
        "Número de Reynolds",
        paragraph("The Reynolds number characterizes the flow regime:"),
        latex(r"\text{Re} = \frac{U L}{\nu}"),
        paragraph(
            "With lid velocity U = 1 and cavity length L = 2, Re = 2/ν. "
            "Higher Re → inertia-dominated (complex vortex structure); "
            "lower Re → viscosity-dominated (simple primary vortex)."
        ),
    ),
    collapsible(
        "Interpretación resultados",
        bullets(
            "Zonas de presión: Los colores representan una escala para la presión del fluido en una región dada.",
            "Vectores de velocidad: Las líneas punteadas representan la dirección y magnitud del movimiento del fluido.",
            "Corriente: Las líneas curvas muestran la forma que adopta el movimiento del fluido, siendo esto en forma de olas.",
        ),
    ),
    collapsible(
        "Parámetros",
        bullets(
            "nx, ny — Coordenadas de espacio (x,y) para la caja delimitadora. El aumentar el tamaño suaviza el comportamiento del fluido, pero vuelve más complicada la operación.",
            "nt — Número de intervalos de tiempo a considerar en el cálculo",
            "nit — Cantidad de iteración a realizar para el cálculo de las zonas de presión. Entre mayores iteraciones, más preciso es el resultado",
            "ρ — Densidad del fluido",
            "ν — Viscosidad cinética",
            "dt — Tamaño de intervalos de tiempo que se consideran para ‘nt’",
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
             "Sheposh, R. (2023). Navier-Stokes equation. EBSCO. https://www.ebsco.com/research-starters/mathematics/navier-stokes-equation",
             "Zhang, J. Xiao, B. Yang, W. (2022, 17 de noviembre). Numerical Study of Lid-Driven Square Cavity Flow with Embedded Circular Obstacles Using Spectral/hp Element Methods. MDPI. https://www.mdpi.com/2076-3417/12/22/11711",
             "Reusken, A. (2012, 06 de enero). Numerical Methods for the Navier-Stokes equations.  RWTH Aachen University. https://www.igpm.rwth-aachen.de/Download/ws1112/numanaIV/NavierStokes.pdf",
        )
    )
]

INFO_CHANNEL_FLOW = [
    paragraph(
        "Channel flow simulates incompressible flow between two parallel plates driven by a "
        "constant body force (analogous to a pressure gradient). Periodic boundary conditions "
        "are applied in x. The steady-state solution is the parabolic Poiseuille profile."
    ),
    collapsible(
        "Governing Equations",
        paragraph("Same Navier-Stokes system as cavity flow, plus a body force F in the x-direction:"),
        latex(
            r"\frac{\partial u}{\partial t} + \ldots = "
            r"-\frac{1}{\rho}\frac{\partial p}{\partial x} + \nu\nabla^2 u + F"
        ),
        paragraph("Periodic BCs in x: outlet connects back to inlet, simulating an infinite channel."),
    ),
    collapsible(
        "Analytical Steady State (Poiseuille Flow)",
        paragraph("Fully developed flow has a parabolic velocity profile:"),
        latex(r"u(y) = \frac{F}{2\nu}\,y\,(L_y - y)"),
        paragraph(
            "The simulation iterates until this steady state is reached or max_steps is exceeded."
        ),
    ),
    collapsible(
        "Parameters",
        bullets(
            "nx, ny — grid dimensions",
            "nit — pressure Poisson iterations per time step",
            "ρ — density",
            "ν — kinematic viscosity",
            "F — body force magnitude (drives the flow)",
            "dt — time step size",
            "Max Iterations — maximum time steps before stopping",
        ),
    ),
]
