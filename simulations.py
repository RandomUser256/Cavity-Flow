import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ─── Shared helpers ────────────────────────────────────────────────────────────

def _dark_1d(fig, title):
    fig.update_layout(
        title=title,
        xaxis_title="x",
        yaxis_title="u(x)",
        template="plotly_dark",
        height=520,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def _dark_3d(fig, title):
    fig.update_layout(title=title, template="plotly_dark", height=580)
    return fig


# ─── 1-D Diffusion ─────────────────────────────────────────────────────────────

def run_1d_diffusion(nx=41, nt=20, nu=0.3, sigma=0.2):
    dx = 2 / (nx - 1)
    dt = sigma * dx ** 2 / nu
    x = np.linspace(0, 2, nx)

    u = np.ones(nx)
    u[int(0.5 / dx): int(1 / dx + 1)] = 2
    u_init = u.copy()

    for _ in range(nt):
        un = u.copy()
        u[1:-1] = un[1:-1] + nu * dt / dx ** 2 * (un[2:] - 2 * un[1:-1] + un[:-2])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=u_init, name="Initial", line=dict(dash="dash", color="#888")))
    fig.add_trace(go.Scatter(x=x, y=u, name=f"After {nt} steps", line=dict(color="#4fc3f7")))
    return _dark_1d(fig, "1D Diffusion Equation")


# ─── 1-D Linear Convection ─────────────────────────────────────────────────────

def run_1d_linear_convection(nx=41, nt=20, c=1.0, sigma=0.5):
    dx = 2 / (nx - 1)
    dt = sigma * dx
    x = np.linspace(0, 2, nx)

    u = np.ones(nx)
    u[int(0.5 / dx): int(1 / dx + 1)] = 2
    u_init = u.copy()

    for _ in range(nt):
        un = u.copy()
        u[1:] = un[1:] - c * dt / dx * (un[1:] - un[:-1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=u_init, name="Initial", line=dict(dash="dash", color="#888")))
    fig.add_trace(go.Scatter(x=x, y=u, name=f"After {nt} steps", line=dict(color="#4fc3f7")))
    return _dark_1d(fig, "1D Linear Convection")


# ─── 1-D Nonlinear Convection ──────────────────────────────────────────────────

def run_1d_nonlinear_convection(nx=41, nt=20, dt=0.025):
    dx = 2 / (nx - 1)
    x = np.linspace(0, 2, nx)

    u = np.ones(nx)
    u[int(0.5 / dx): int(1 / dx + 1)] = 2
    u_init = u.copy()

    for _ in range(nt):
        un = u.copy()
        u[1:] = un[1:] - un[1:] * dt / dx * (un[1:] - un[:-1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=u_init, name="Initial", line=dict(dash="dash", color="#888")))
    fig.add_trace(go.Scatter(x=x, y=u, name=f"After {nt} steps", line=dict(color="#4fc3f7")))
    return _dark_1d(fig, "1D Nonlinear Convection")


# ─── 1-D Burgers ───────────────────────────────────────────────────────────────

def run_burgers_1d(nx=101, nt=100, nu=0.07):
    import sympy
    from sympy.utilities.lambdify import lambdify

    x_s, nu_s, t_s = sympy.symbols("x nu t")
    phi = (
        sympy.exp(-((x_s - 4 * t_s) ** 2) / (4 * nu_s * (t_s + 1)))
        + sympy.exp(-((x_s - 4 * t_s - 2 * sympy.pi) ** 2) / (4 * nu_s * (t_s + 1)))
    )
    u_sym = -2 * nu_s * (phi.diff(x_s) / phi) + 4
    ufunc = lambdify((t_s, x_s, nu_s), u_sym)

    dx = 2 * np.pi / (nx - 1)
    dt = dx * nu
    x = np.linspace(0, 2 * np.pi, nx)

    u = np.asarray([ufunc(0, x0, nu) for x0 in x], dtype=float)
    u_init = u.copy()

    for _ in range(nt):
        un = u.copy()
        u[1:-1] = (
            un[1:-1]
            - un[1:-1] * dt / dx * (un[1:-1] - un[:-2])
            + nu * dt / dx ** 2 * (un[2:] - 2 * un[1:-1] + un[:-2])
        )
        u[0] = (
            un[0]
            - un[0] * dt / dx * (un[0] - un[-2])
            + nu * dt / dx ** 2 * (un[1] - 2 * un[0] + un[-2])
        )
        u[-1] = u[0]

    u_analytical = np.asarray([ufunc(nt * dt, xi, nu) for xi in x], dtype=float)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=u_init, name="Initial", line=dict(dash="dash", color="#888")))
    fig.add_trace(
        go.Scatter(x=x, y=u, name="Numerical", mode="lines+markers",
                   line=dict(color="#4fc3f7"), marker=dict(size=3))
    )
    fig.add_trace(go.Scatter(x=x, y=u_analytical, name="Analytical", line=dict(color="#ef5350", dash="dot")))
    fig.update_layout(
        title="1D Burgers Equation",
        xaxis_title="x", yaxis_title="u(x)",
        xaxis_range=[0, 2 * np.pi], yaxis_range=[0, 10],
        template="plotly_dark", height=520,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


# ─── 2-D Laplace ───────────────────────────────────────────────────────────────

def run_2d_laplace(nx=31, ny=31, l1norm_target=1e-4):
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 1, ny)

    p = np.zeros((ny, nx))
    p[:, 0] = 0
    p[:, -1] = y
    p[0, :] = p[1, :]
    p[-1, :] = p[-2, :]

    l1norm = 1.0
    max_iter = 10_000
    it = 0
    while l1norm > l1norm_target and it < max_iter:
        pn = p.copy()
        p[1:-1, 1:-1] = (
            dy ** 2 * (pn[1:-1, 2:] + pn[1:-1, :-2])
            + dx ** 2 * (pn[2:, 1:-1] + pn[:-2, 1:-1])
        ) / (2 * (dx ** 2 + dy ** 2))
        p[:, 0] = 0
        p[:, -1] = y
        p[0, :] = p[1, :]
        p[-1, :] = p[-2, :]
        denom = np.sum(np.abs(pn))
        if denom < 1e-14:
            break
        l1norm = np.sum(np.abs(p) - np.abs(pn)) / denom
        it += 1

    X, Y = np.meshgrid(x, y)
    fig = go.Figure(go.Surface(x=X, y=Y, z=p, colorscale="Viridis"))
    fig.update_layout(
        title="2D Laplace Equation",
        scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="p"),
        template="plotly_dark", height=580,
    )
    return fig


# ─── 2-D Poisson ───────────────────────────────────────────────────────────────

def run_2d_poisson(nx=50, ny=50, nt=100):
    dx = 2 / (nx - 1)
    dy = 1 / (ny - 1)
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 1, ny)

    p = np.zeros((ny, nx))
    b = np.zeros((ny, nx))
    b[int(ny / 4), int(nx / 4)] = 100
    b[int(3 * ny / 4), int(3 * nx / 4)] = -100

    for _ in range(nt):
        pd = p.copy()
        p[1:-1, 1:-1] = (
            (pd[1:-1, 2:] + pd[1:-1, :-2]) * dy ** 2
            + (pd[2:, 1:-1] + pd[:-2, 1:-1]) * dx ** 2
            - b[1:-1, 1:-1] * dx ** 2 * dy ** 2
        ) / (2 * (dx ** 2 + dy ** 2))
        p[0, :] = 0
        p[-1, :] = 0
        p[:, 0] = 0
        p[:, -1] = 0

    X, Y = np.meshgrid(x, y)
    fig = go.Figure(go.Surface(x=X, y=Y, z=p, colorscale="RdBu"))
    fig.update_layout(
        title="2D Poisson Equation",
        scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="p"),
        template="plotly_dark", height=580,
    )
    return fig


# ─── 2-D Diffusion ─────────────────────────────────────────────────────────────

def run_2d_diffusion(nx=31, ny=31, nt=50, nu=0.05, sigma=0.25):
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    dt = sigma * dx * dy / nu
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 2, ny)

    u = np.ones((ny, nx))
    u[int(0.5 / dy): int(1 / dy + 1), int(0.5 / dx): int(1 / dx + 1)] = 2
    u_init = u.copy()

    for _ in range(nt + 1):
        un = u.copy()
        u[1:-1, 1:-1] = (
            un[1:-1, 1:-1]
            + nu * dt / dx ** 2 * (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, :-2])
            + nu * dt / dy ** 2 * (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[:-2, 1:-1])
        )
        u[0, :] = 1; u[-1, :] = 1
        u[:, 0] = 1; u[:, -1] = 1

    X, Y = np.meshgrid(x, y)
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "surface"}, {"type": "surface"}]],
        subplot_titles=["Initial Condition", f"After {nt} Steps"],
    )
    fig.add_trace(go.Surface(x=X, y=Y, z=u_init, colorscale="Viridis", showscale=False), row=1, col=1)
    fig.add_trace(go.Surface(x=X, y=Y, z=u, colorscale="Viridis"), row=1, col=2)
    return _dark_3d(fig, "2D Diffusion Equation")


# ─── 2-D Linear Convection ─────────────────────────────────────────────────────

def run_2d_linear_convection(nx=81, ny=81, nt=100, c=1.0, sigma=0.2):
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    dt = sigma * dx
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 2, ny)

    u = np.ones((ny, nx))
    u[int(0.5 / dy): int(1 / dy + 1), int(0.5 / dx): int(1 / dx + 1)] = 2
    u_init = u.copy()

    for _ in range(nt + 1):
        un = u.copy()
        u[1:, 1:] = (
            un[1:, 1:]
            - c * dt / dx * (un[1:, 1:] - un[1:, :-1])
            - c * dt / dy * (un[1:, 1:] - un[:-1, 1:])
        )
        u[0, :] = 1; u[-1, :] = 1
        u[:, 0] = 1; u[:, -1] = 1

    X, Y = np.meshgrid(x, y)
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "surface"}, {"type": "surface"}]],
        subplot_titles=["Initial Condition", f"After {nt} Steps"],
    )
    fig.add_trace(go.Surface(x=X, y=Y, z=u_init, colorscale="Viridis", showscale=False), row=1, col=1)
    fig.add_trace(go.Surface(x=X, y=Y, z=u, colorscale="Viridis"), row=1, col=2)
    return _dark_3d(fig, "2D Linear Convection")


# ─── 2-D Nonlinear Convection ──────────────────────────────────────────────────

def run_2d_nonlinear_convection(nx=101, ny=101, nt=80, sigma=0.2):
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    dt = sigma * dx
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 2, ny)

    u = np.ones((ny, nx))
    v = np.ones((ny, nx))
    u[int(0.5 / dy): int(1 / dy + 1), int(0.5 / dx): int(1 / dx + 1)] = 2
    v[int(0.5 / dy): int(1 / dy + 1), int(0.5 / dx): int(1 / dx + 1)] = 2

    for _ in range(nt + 1):
        un = u.copy(); vn = v.copy()
        u[1:, 1:] = (
            un[1:, 1:]
            - un[1:, 1:] * dt / dx * (un[1:, 1:] - un[1:, :-1])
            - vn[1:, 1:] * dt / dy * (un[1:, 1:] - un[:-1, 1:])
        )
        v[1:, 1:] = (
            vn[1:, 1:]
            - un[1:, 1:] * dt / dx * (vn[1:, 1:] - vn[1:, :-1])
            - vn[1:, 1:] * dt / dy * (vn[1:, 1:] - vn[:-1, 1:])
        )
        u[0, :] = 1; u[-1, :] = 1; u[:, 0] = 1; u[:, -1] = 1
        v[0, :] = 1; v[-1, :] = 1; v[:, 0] = 1; v[:, -1] = 1

    X, Y = np.meshgrid(x, y)
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "surface"}, {"type": "surface"}]],
        subplot_titles=["u-velocity", "v-velocity"],
    )
    fig.add_trace(go.Surface(x=X, y=Y, z=u, colorscale="Viridis", showscale=False), row=1, col=1)
    fig.add_trace(go.Surface(x=X, y=Y, z=v, colorscale="Plasma"), row=1, col=2)
    return _dark_3d(fig, "2D Nonlinear Convection")


# ─── 2-D Burgers ───────────────────────────────────────────────────────────────

def run_burgers_2d(nx=41, ny=41, nt=120, nu=0.01, sigma=0.0009):
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    dt = sigma * dx * dy / nu
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 2, ny)

    u = np.ones((ny, nx))
    v = np.ones((ny, nx))
    u[int(0.5 / dy): int(1 / dy + 1), int(0.5 / dx): int(1 / dx + 1)] = 2
    v[int(0.5 / dy): int(1 / dy + 1), int(0.5 / dx): int(1 / dx + 1)] = 2

    for _ in range(nt + 1):
        un = u.copy(); vn = v.copy()
        u[1:-1, 1:-1] = (
            un[1:-1, 1:-1]
            - dt / dx * un[1:-1, 1:-1] * (un[1:-1, 1:-1] - un[1:-1, :-2])
            - dt / dy * vn[1:-1, 1:-1] * (un[1:-1, 1:-1] - un[:-2, 1:-1])
            + nu * dt / dx ** 2 * (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, :-2])
            + nu * dt / dy ** 2 * (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[:-2, 1:-1])
        )
        v[1:-1, 1:-1] = (
            vn[1:-1, 1:-1]
            - dt / dx * un[1:-1, 1:-1] * (vn[1:-1, 1:-1] - vn[1:-1, :-2])
            - dt / dy * vn[1:-1, 1:-1] * (vn[1:-1, 1:-1] - vn[:-2, 1:-1])
            + nu * dt / dx ** 2 * (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, :-2])
            + nu * dt / dy ** 2 * (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[:-2, 1:-1])
        )
        u[0, :] = 1; u[-1, :] = 1; u[:, 0] = 1; u[:, -1] = 1
        v[0, :] = 1; v[-1, :] = 1; v[:, 0] = 1; v[:, -1] = 1

    X, Y = np.meshgrid(x, y)
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "surface"}, {"type": "surface"}]],
        subplot_titles=["u-velocity", "v-velocity"],
    )
    fig.add_trace(go.Surface(x=X, y=Y, z=u, colorscale="Viridis", showscale=False), row=1, col=1)
    fig.add_trace(go.Surface(x=X, y=Y, z=v, colorscale="Plasma"), row=1, col=2)
    return _dark_3d(fig, "2D Burgers Equation")


# ─── Cavity Flow (Navier-Stokes) ───────────────────────────────────────────────

def _build_b_cavity(rho, dt, dx, dy, u, v):
    b = np.zeros_like(u)
    b[1:-1, 1:-1] = rho * (
        1 / dt * (
            (u[1:-1, 2:] - u[1:-1, :-2]) / (2 * dx)
            + (v[2:, 1:-1] - v[:-2, 1:-1]) / (2 * dy)
        )
        - ((u[1:-1, 2:] - u[1:-1, :-2]) / (2 * dx)) ** 2
        - 2 * (
            (u[2:, 1:-1] - u[:-2, 1:-1]) / (2 * dy)
            * (v[1:-1, 2:] - v[1:-1, :-2]) / (2 * dx)
        )
        - ((v[2:, 1:-1] - v[:-2, 1:-1]) / (2 * dy)) ** 2
    )
    return b


def _pressure_poisson_cavity(p, dx, dy, b, nit):
    for _ in range(nit):
        pn = p.copy()
        p[1:-1, 1:-1] = (
            ((pn[1:-1, 2:] + pn[1:-1, :-2]) * dy ** 2
             + (pn[2:, 1:-1] + pn[:-2, 1:-1]) * dx ** 2)
            / (2 * (dx ** 2 + dy ** 2))
            - dx ** 2 * dy ** 2 / (2 * (dx ** 2 + dy ** 2)) * b[1:-1, 1:-1]
        )
        p[:, -1] = p[:, -2]   # dp/dx = 0 at x = 2
        p[0, :] = p[1, :]     # dp/dy = 0 at y = 0
        p[:, 0] = p[:, 1]     # dp/dx = 0 at x = 0
        p[-1, :] = 0          # p = 0 at y = 2 (lid)
    return p


def run_cavity_flow(nx=41, ny=41, nt=500, nit=50, rho=1.0, nu=0.1, dt=0.001):
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 2, ny)

    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.zeros((ny, nx))
    b = np.zeros((ny, nx))

    for _ in range(nt):
        un = u.copy(); vn = v.copy()
        b = _build_b_cavity(rho, dt, dx, dy, u, v)
        p = _pressure_poisson_cavity(p, dx, dy, b, nit)

        u[1:-1, 1:-1] = (
            un[1:-1, 1:-1]
            - un[1:-1, 1:-1] * dt / dx * (un[1:-1, 1:-1] - un[1:-1, :-2])
            - vn[1:-1, 1:-1] * dt / dy * (un[1:-1, 1:-1] - un[:-2, 1:-1])
            - dt / (2 * rho * dx) * (p[1:-1, 2:] - p[1:-1, :-2])
            + nu * (
                dt / dx ** 2 * (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, :-2])
                + dt / dy ** 2 * (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[:-2, 1:-1])
            )
        )
        v[1:-1, 1:-1] = (
            vn[1:-1, 1:-1]
            - un[1:-1, 1:-1] * dt / dx * (vn[1:-1, 1:-1] - vn[1:-1, :-2])
            - vn[1:-1, 1:-1] * dt / dy * (vn[1:-1, 1:-1] - vn[:-2, 1:-1])
            - dt / (2 * rho * dy) * (p[2:, 1:-1] - p[:-2, 1:-1])
            + nu * (
                dt / dx ** 2 * (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, :-2])
                + dt / dy ** 2 * (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[:-2, 1:-1])
            )
        )
        u[0, :] = 0; u[:, 0] = 0; u[:, -1] = 0
        u[-1, :] = 1
        v[0, :] = 0; v[-1, :] = 0; v[:, 0] = 0; v[:, -1] = 0

    # Streamfunction (integrate u along y)
    psi = np.cumsum(u * dy, axis=0)

    # Quiver arrows on a coarse sub-grid
    step = max(2, nx // 20)
    X, Y = np.meshgrid(x, y)
    xs = X[::step, ::step].flatten()
    ys = Y[::step, ::step].flatten()
    us = u[::step, ::step].flatten()
    vs = v[::step, ::step].flatten()

    scale = 0.08
    ax, ay = [], []
    for xi, yi, ui, vi in zip(xs, ys, us, vs):
        ax += [xi, xi + ui * scale, None]
        ay += [yi, yi + vi * scale, None]

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Pressure + Velocity Vectors", "Stream Function (ψ)"],
    )
    fig.add_trace(
        go.Contour(x=x, y=y, z=p, colorscale="Viridis", showscale=True,
                   contours=dict(coloring="heatmap"), name="Pressure"),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(x=ax, y=ay, mode="lines",
                   line=dict(color="white", width=1), showlegend=False),
        row=1, col=1,
    )
    fig.add_trace(
        go.Contour(x=x, y=y, z=psi, colorscale="Plasma", showscale=True,
                   ncontours=30, name="ψ"),
        row=1, col=2,
    )
    fig.update_layout(title="Cavity Flow — Navier-Stokes", template="plotly_dark", height=560)
    return fig


# ─── Channel Flow (Navier-Stokes, periodic) ────────────────────────────────────

def _build_b_channel(rho, dt, dx, dy, u, v):
    b = np.zeros_like(u)
    b[1:-1, 1:-1] = rho * (
        1 / dt * (
            (u[1:-1, 2:] - u[1:-1, :-2]) / (2 * dx)
            + (v[2:, 1:-1] - v[:-2, 1:-1]) / (2 * dy)
        )
        - ((u[1:-1, 2:] - u[1:-1, :-2]) / (2 * dx)) ** 2
        - 2 * (
            (u[2:, 1:-1] - u[:-2, 1:-1]) / (2 * dy)
            * (v[1:-1, 2:] - v[1:-1, :-2]) / (2 * dx)
        )
        - ((v[2:, 1:-1] - v[:-2, 1:-1]) / (2 * dy)) ** 2
    )
    # Periodic at x = 2
    b[1:-1, -1] = rho * (
        1 / dt * (
            (u[1:-1, 0] - u[1:-1, -2]) / (2 * dx)
            + (v[2:, -1] - v[:-2, -1]) / (2 * dy)
        )
        - ((u[1:-1, 0] - u[1:-1, -2]) / (2 * dx)) ** 2
        - 2 * (
            (u[2:, -1] - u[:-2, -1]) / (2 * dy)
            * (v[1:-1, 0] - v[1:-1, -2]) / (2 * dx)
        )
        - ((v[2:, -1] - v[:-2, -1]) / (2 * dy)) ** 2
    )
    # Periodic at x = 0
    b[1:-1, 0] = rho * (
        1 / dt * (
            (u[1:-1, 1] - u[1:-1, -1]) / (2 * dx)
            + (v[2:, 0] - v[:-2, 0]) / (2 * dy)
        )
        - ((u[1:-1, 1] - u[1:-1, -1]) / (2 * dx)) ** 2
        - 2 * (
            (u[2:, 0] - u[:-2, 0]) / (2 * dy)
            * (v[1:-1, 1] - v[1:-1, -1]) / (2 * dx)
        )
        - ((v[2:, 0] - v[:-2, 0]) / (2 * dy)) ** 2
    )
    return b


def _pressure_poisson_periodic(p, dx, dy, b, nit):
    for _ in range(nit):
        pn = p.copy()
        p[1:-1, 1:-1] = (
            ((pn[1:-1, 2:] + pn[1:-1, :-2]) * dy ** 2
             + (pn[2:, 1:-1] + pn[:-2, 1:-1]) * dx ** 2)
            / (2 * (dx ** 2 + dy ** 2))
            - dx ** 2 * dy ** 2 / (2 * (dx ** 2 + dy ** 2)) * b[1:-1, 1:-1]
        )
        p[1:-1, -1] = (
            ((pn[1:-1, 0] + pn[1:-1, -2]) * dy ** 2
             + (pn[2:, -1] + pn[:-2, -1]) * dx ** 2)
            / (2 * (dx ** 2 + dy ** 2))
            - dx ** 2 * dy ** 2 / (2 * (dx ** 2 + dy ** 2)) * b[1:-1, -1]
        )
        p[1:-1, 0] = (
            ((pn[1:-1, 1] + pn[1:-1, -1]) * dy ** 2
             + (pn[2:, 0] + pn[:-2, 0]) * dx ** 2)
            / (2 * (dx ** 2 + dy ** 2))
            - dx ** 2 * dy ** 2 / (2 * (dx ** 2 + dy ** 2)) * b[1:-1, 0]
        )
        p[-1, :] = p[-2, :]
        p[0, :] = p[1, :]
    return p


def run_channel_flow(nx=41, ny=41, nit=50, rho=1.0, nu=0.1, F=1.0, dt=0.01, max_steps=500):
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 2, ny)

    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.ones((ny, nx))
    b = np.zeros((ny, nx))

    udiff = 1.0
    stepcount = 0

    while udiff > 0.001 and stepcount < max_steps:
        un = u.copy(); vn = v.copy()
        b = _build_b_channel(rho, dt, dx, dy, u, v)
        p = _pressure_poisson_periodic(p, dx, dy, b, nit)

        u[1:-1, 1:-1] = (
            un[1:-1, 1:-1]
            - un[1:-1, 1:-1] * dt / dx * (un[1:-1, 1:-1] - un[1:-1, :-2])
            - vn[1:-1, 1:-1] * dt / dy * (un[1:-1, 1:-1] - un[:-2, 1:-1])
            - dt / (2 * rho * dx) * (p[1:-1, 2:] - p[1:-1, :-2])
            + nu * (
                dt / dx ** 2 * (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, :-2])
                + dt / dy ** 2 * (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[:-2, 1:-1])
            )
            + F * dt
        )
        v[1:-1, 1:-1] = (
            vn[1:-1, 1:-1]
            - un[1:-1, 1:-1] * dt / dx * (vn[1:-1, 1:-1] - vn[1:-1, :-2])
            - vn[1:-1, 1:-1] * dt / dy * (vn[1:-1, 1:-1] - vn[:-2, 1:-1])
            - dt / (2 * rho * dy) * (p[2:, 1:-1] - p[:-2, 1:-1])
            + nu * (
                dt / dx ** 2 * (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, :-2])
                + dt / dy ** 2 * (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[:-2, 1:-1])
            )
        )
        # Periodic BC u @ x = 2
        u[1:-1, -1] = (
            un[1:-1, -1]
            - un[1:-1, -1] * dt / dx * (un[1:-1, -1] - un[1:-1, -2])
            - vn[1:-1, -1] * dt / dy * (un[1:-1, -1] - un[:-2, -1])
            - dt / (2 * rho * dx) * (p[1:-1, 0] - p[1:-1, -2])
            + nu * (
                dt / dx ** 2 * (un[1:-1, 0] - 2 * un[1:-1, -1] + un[1:-1, -2])
                + dt / dy ** 2 * (un[2:, -1] - 2 * un[1:-1, -1] + un[:-2, -1])
            )
            + F * dt
        )
        # Periodic BC u @ x = 0
        u[1:-1, 0] = (
            un[1:-1, 0]
            - un[1:-1, 0] * dt / dx * (un[1:-1, 0] - un[1:-1, -1])
            - vn[1:-1, 0] * dt / dy * (un[1:-1, 0] - un[:-2, 0])
            - dt / (2 * rho * dx) * (p[1:-1, 1] - p[1:-1, -1])
            + nu * (
                dt / dx ** 2 * (un[1:-1, 1] - 2 * un[1:-1, 0] + un[1:-1, -1])
                + dt / dy ** 2 * (un[2:, 0] - 2 * un[1:-1, 0] + un[:-2, 0])
            )
            + F * dt
        )
        # Periodic BC v @ x = 2
        v[1:-1, -1] = (
            vn[1:-1, -1]
            - un[1:-1, -1] * dt / dx * (vn[1:-1, -1] - vn[1:-1, -2])
            - vn[1:-1, -1] * dt / dy * (vn[1:-1, -1] - vn[:-2, -1])
            - dt / (2 * rho * dy) * (p[2:, -1] - p[:-2, -1])
            + nu * (
                dt / dx ** 2 * (vn[1:-1, 0] - 2 * vn[1:-1, -1] + vn[1:-1, -2])
                + dt / dy ** 2 * (vn[2:, -1] - 2 * vn[1:-1, -1] + vn[:-2, -1])
            )
        )
        # Periodic BC v @ x = 0
        v[1:-1, 0] = (
            vn[1:-1, 0]
            - un[1:-1, 0] * dt / dx * (vn[1:-1, 0] - vn[1:-1, -1])
            - vn[1:-1, 0] * dt / dy * (vn[1:-1, 0] - vn[:-2, 0])
            - dt / (2 * rho * dy) * (p[2:, 0] - p[:-2, 0])
            + nu * (
                dt / dx ** 2 * (vn[1:-1, 1] - 2 * vn[1:-1, 0] + vn[1:-1, -1])
                + dt / dy ** 2 * (vn[2:, 0] - 2 * vn[1:-1, 0] + vn[:-2, 0])
            )
        )
        u[0, :] = 0; u[-1, :] = 0
        v[0, :] = 0; v[-1, :] = 0

        s = np.sum(u)
        udiff = (s - np.sum(un)) / s if s != 0 else 0.0
        stepcount += 1

    X, Y = np.meshgrid(x, y)
    step = max(3, nx // 15)
    xs = X[::step, ::step].flatten()
    ys = Y[::step, ::step].flatten()
    us = u[::step, ::step].flatten()
    vs = v[::step, ::step].flatten()

    scale = 0.12
    ax, ay = [], []
    for xi, yi, ui, vi in zip(xs, ys, us, vs):
        ax += [xi, xi + ui * scale, None]
        ay += [yi, yi + vi * scale, None]

    speed = np.sqrt(u ** 2 + v ** 2)
    fig = go.Figure()
    fig.add_trace(go.Contour(x=x, y=y, z=speed, colorscale="Viridis", showscale=True, name="Speed"))
    fig.add_trace(
        go.Scatter(x=ax, y=ay, mode="lines",
                   line=dict(color="white", width=1), showlegend=False)
    )
    fig.update_layout(
        title=f"Channel Flow — Navier-Stokes  (converged in {stepcount} steps)",
        xaxis_title="x", yaxis_title="y",
        template="plotly_dark", height=540,
    )
    return fig
