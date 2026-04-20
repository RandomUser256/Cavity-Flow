"""
2D numerical solvers for various PDEs.
Functions return numerical solutions as numpy arrays without plotting.
"""

import numpy as np
from typing import Tuple, Dict
from .utils import apply_boundary_conditions_2d


def linear_convection_2d(
    nx: int = 101,
    ny: int = 101,
    nt: int = 80,
    domain_x: Tuple[float, float] = (0.0, 2.0),
    domain_y: Tuple[float, float] = (0.0, 2.0),
    c: float = 1.0,
    sigma: float = 0.2,
    initial_condition: np.ndarray = None
) -> Dict[str, np.ndarray]:
    """
    Solve 2D linear convection equation: du/dt + c*(du/dx + du/dy) = 0
    
    Parameters
    ----------
    nx, ny : int
        Number of spatial grid points in x and y
    nt : int
        Number of time steps
    domain_x, domain_y : Tuple[float, float]
        Domain bounds (start, end) for x and y
    c : float
        Wave speed
    sigma : float
        CFL coefficient
    initial_condition : np.ndarray, optional
        Custom initial condition. If None, uses 2D hat function
        
    Returns
    -------
    Dict[str, np.ndarray]
        'x': x grid points
        'y': y grid points
        'u': final solution (ny x nx)
        'history': solution history
    """
    dx = (domain_x[1] - domain_x[0]) / (nx - 1)
    dy = (domain_y[1] - domain_y[0]) / (ny - 1)
    dt = sigma * min(dx, dy) / c
    
    x = np.linspace(domain_x[0], domain_x[1], nx)
    y = np.linspace(domain_y[0], domain_y[1], ny)
    
    # Initialize solution
    if initial_condition is None:
        u = np.ones((ny, nx))
        v = np.ones((ny, nx))
        # Hat function ICs
        u[int(0.5/dy):int(1.0/dy+1), int(0.5/dx):int(1.0/dx+1)] = 2.0
        v[int(0.5/dy):int(1.0/dy+1), int(0.5/dx):int(1.0/dx+1)] = 2.0
    else:
        u = initial_condition.copy()
        v = initial_condition.copy()
    
    un = np.ones((ny, nx))
    vn = np.ones((ny, nx))
    history = np.zeros((nt + 1, ny, nx))
    history[0, :, :] = u
    
    # Time stepping
    for n in range(nt):
        un = u.copy()
        vn = v.copy()
        
        u[1:, 1:] = (un[1:, 1:] - 
                     (un[1:, 1:] * c * dt / dx * (un[1:, 1:] - un[1:, :-1])) -
                     (vn[1:, 1:] * c * dt / dy * (un[1:, 1:] - un[:-1, 1:])))
        
        v[1:, 1:] = (vn[1:, 1:] -
                     (un[1:, 1:] * c * dt / dx * (vn[1:, 1:] - vn[1:, :-1])) -
                     (vn[1:, 1:] * c * dt / dy * (vn[1:, 1:] - vn[:-1, 1:])))
        
        # Boundary conditions
        u[0, :] = 1.0
        u[-1, :] = 1.0
        u[:, 0] = 1.0
        u[:, -1] = 1.0
        
        v[0, :] = 1.0
        v[-1, :] = 1.0
        v[:, 0] = 1.0
        v[:, -1] = 1.0
        
        history[n + 1, :, :] = u
    
    return {
        'x': x,
        'y': y,
        'u': u,
        'v': v,
        'history': history,
        'dx': dx,
        'dy': dy,
        'dt': dt,
        't_final': nt * dt
    }


def nonlinear_convection_2d(
    nx: int = 101,
    ny: int = 101,
    nt: int = 80,
    domain_x: Tuple[float, float] = (0.0, 2.0),
    domain_y: Tuple[float, float] = (0.0, 2.0),
    c: float = 1.0,
    sigma: float = 0.2,
    initial_condition: np.ndarray = None
) -> Dict[str, np.ndarray]:
    """
    Solve 2D nonlinear convection equation: du/dt + u*du/dx + v*du/dy = 0
    
    Parameters
    ----------
    nx, ny : int
        Number of spatial grid points
    nt : int
        Number of time steps
    domain_x, domain_y : Tuple[float, float]
        Domain bounds
    c : float
        Wave speed coefficient
    sigma : float
        CFL coefficient
    initial_condition : np.ndarray, optional
        Custom initial condition
        
    Returns
    -------
    Dict[str, np.ndarray]
        'x': x grid points
        'y': y grid points
        'u': final solution
        'v': final v component
        'history': solution history
    """
    dx = (domain_x[1] - domain_x[0]) / (nx - 1)
    dy = (domain_y[1] - domain_y[0]) / (ny - 1)
    dt = sigma * min(dx, dy)
    
    x = np.linspace(domain_x[0], domain_x[1], nx)
    y = np.linspace(domain_y[0], domain_y[1], ny)
    
    # Initialize solution
    if initial_condition is None:
        u = np.ones((ny, nx))
        v = np.ones((ny, nx))
        u[int(0.5/dy):int(1.0/dy+1), int(0.5/dx):int(1.0/dx+1)] = 2.0
        v[int(0.5/dy):int(1.0/dy+1), int(0.5/dx):int(1.0/dx+1)] = 2.0
    else:
        u = initial_condition.copy()
        v = initial_condition.copy()
    
    un = np.ones((ny, nx))
    vn = np.ones((ny, nx))
    history = np.zeros((nt + 1, ny, nx))
    history[0, :, :] = u
    
    # Time stepping
    for n in range(nt):
        un = u.copy()
        vn = v.copy()
        
        u[1:, 1:] = (un[1:, 1:] -
                     (un[1:, 1:] * c * dt / dx * (un[1:, 1:] - un[1:, :-1])) -
                     (vn[1:, 1:] * c * dt / dy * (un[1:, 1:] - un[:-1, 1:])))
        
        v[1:, 1:] = (vn[1:, 1:] -
                     (un[1:, 1:] * c * dt / dx * (vn[1:, 1:] - vn[1:, :-1])) -
                     (vn[1:, 1:] * c * dt / dy * (vn[1:, 1:] - vn[:-1, 1:])))
        
        # Boundary conditions
        u[0, :] = 1.0
        u[-1, :] = 1.0
        u[:, 0] = 1.0
        u[:, -1] = 1.0
        
        v[0, :] = 1.0
        v[-1, :] = 1.0
        v[:, 0] = 1.0
        v[:, -1] = 1.0
        
        history[n + 1, :, :] = u
    
    return {
        'x': x,
        'y': y,
        'u': u,
        'v': v,
        'history': history,
        'dx': dx,
        'dy': dy,
        'dt': dt,
        't_final': nt * dt
    }


def diffusion_2d(
    nx: int = 31,
    ny: int = 31,
    nt: int = 17,
    domain_x: Tuple[float, float] = (0.0, 2.0),
    domain_y: Tuple[float, float] = (0.0, 2.0),
    nu: float = 0.05,
    sigma: float = 0.25,
    initial_condition: np.ndarray = None
) -> Dict[str, np.ndarray]:
    """
    Solve 2D diffusion (heat) equation: du/dt = nu*(d²u/dx² + d²u/dy²)
    
    Parameters
    ----------
    nx, ny : int
        Number of spatial grid points
    nt : int
        Number of time steps
    domain_x, domain_y : Tuple[float, float]
        Domain bounds
    nu : float
        Diffusion coefficient
    sigma : float
        Stability parameter
    initial_condition : np.ndarray, optional
        Custom initial condition
        
    Returns
    -------
    Dict[str, np.ndarray]
        'x': x grid points
        'y': y grid points
        'u': final solution
        'history': solution history
    """
    dx = (domain_x[1] - domain_x[0]) / (nx - 1)
    dy = (domain_y[1] - domain_y[0]) / (ny - 1)
    dt = sigma * dx * dy / nu
    
    x = np.linspace(domain_x[0], domain_x[1], nx)
    y = np.linspace(domain_y[0], domain_y[1], ny)
    
    # Initialize solution
    if initial_condition is None:
        u = np.ones((ny, nx))
        u[int(0.5/dy):int(1.0/dy+1), int(0.5/dx):int(1.0/dx+1)] = 2.0
    else:
        u = initial_condition.copy()
    
    un = np.ones((ny, nx))
    history = np.zeros((nt + 1, ny, nx))
    history[0, :, :] = u
    
    # Time stepping
    for n in range(nt):
        un = u.copy()
        u[1:-1, 1:-1] = (un[1:-1, 1:-1] +
                         nu * dt / dx**2 * (un[1:-1, 2:] - 2*un[1:-1, 1:-1] + un[1:-1, :-2]) +
                         nu * dt / dy**2 * (un[2:, 1:-1] - 2*un[1:-1, 1:-1] + un[:-2, 1:-1]))
        
        # Boundary conditions
        u[0, :] = 1.0
        u[-1, :] = 1.0
        u[:, 0] = 1.0
        u[:, -1] = 1.0
        
        history[n + 1, :, :] = u
    
    return {
        'x': x,
        'y': y,
        'u': u,
        'history': history,
        'dx': dx,
        'dy': dy,
        'dt': dt,
        't_final': nt * dt,
        'nu': nu
    }


def laplace_2d(
    nx: int = 31,
    ny: int = 31,
    domain_x: Tuple[float, float] = (0.0, 2.0),
    domain_y: Tuple[float, float] = (0.0, 1.0),
    l1norm_target: float = 1e-4,
    max_iterations: int = 10000
) -> Dict[str, np.ndarray]:
    """
    Solve 2D Laplace equation using iterative method.
    ∇²p = 0
    
    Parameters
    ----------
    nx, ny : int
        Number of spatial grid points
    domain_x, domain_y : Tuple[float, float]
        Domain bounds
    l1norm_target : float
        Convergence tolerance (L1 norm of difference)
    max_iterations : int
        Maximum number of iterations
        
    Returns
    -------
    Dict[str, np.ndarray]
        'x': x grid points
        'y': y grid points
        'p': final solution
        'iterations': number of iterations performed
    """
    dx = (domain_x[1] - domain_x[0]) / (nx - 1)
    dy = (domain_y[1] - domain_y[0]) / (ny - 1)
    
    x = np.linspace(domain_x[0], domain_x[1], nx)
    y = np.linspace(domain_y[0], domain_y[1], ny)
    
    p = np.zeros((ny, nx))
    pn = np.empty_like(p)
    
    # Boundary conditions
    p[:, 0] = 0.0           # p = 0 @ x = 0
    p[:, -1] = y            # p = y @ x = 2
    p[0, :] = p[1, :]       # dp/dy = 0 @ y = 0
    p[-1, :] = p[-2, :]     # dp/dy = 0 @ y = 1
    
    l1norm = 1.0
    iteration = 0
    
    # Iterative solver
    while l1norm > l1norm_target and iteration < max_iterations:
        pn = p.copy()
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, :-2]) * dy**2 +
                          (pn[2:, 1:-1] + pn[:-2, 1:-1]) * dx**2) /
                         (2 * (dx**2 + dy**2)))
        
        # Boundary conditions
        p[:, 0] = 0.0
        p[:, -1] = y
        p[0, :] = p[1, :]
        p[-1, :] = p[-2, :]
        
        l1norm = (np.sum(np.abs(p[:]) - np.abs(pn[:])) /
                  np.sum(np.abs(pn[:])))
        iteration += 1
    
    return {
        'x': x,
        'y': y,
        'p': p,
        'iterations': iteration,
        'dx': dx,
        'dy': dy,
        'converged': l1norm <= l1norm_target
    }


def poisson_2d(
    nx: int = 50,
    ny: int = 50,
    nt: int = 100,
    domain_x: Tuple[float, float] = (0.0, 2.0),
    domain_y: Tuple[float, float] = (0.0, 1.0),
    source_term: np.ndarray = None
) -> Dict[str, np.ndarray]:
    """
    Solve 2D Poisson equation using iterative method.
    ∇²p = b (where b is source term)
    
    Parameters
    ----------
    nx, ny : int
        Number of spatial grid points
    nt : int
        Number of iterations
    domain_x, domain_y : Tuple[float, float]
        Domain bounds
    source_term : np.ndarray, optional
        Source term b. If None, creates default localized sources
        
    Returns
    -------
    Dict[str, np.ndarray]
        'x': x grid points
        'y': y grid points
        'p': final solution
    """
    dx = (domain_x[1] - domain_x[0]) / (nx - 1)
    dy = (domain_y[1] - domain_y[0]) / (ny - 1)
    
    x = np.linspace(domain_x[0], domain_x[1], nx)
    y = np.linspace(domain_y[0], domain_y[1], ny)
    
    p = np.zeros((ny, nx))
    pd = np.zeros((ny, nx))
    
    # Source term
    if source_term is None:
        b = np.zeros((ny, nx))
        b[int(ny / 4), int(nx / 4)] = 100
        b[int(3 * ny / 4), int(3 * nx / 4)] = -100
    else:
        b = source_term.copy()
    
    # Iterative solver
    for it in range(nt):
        pd = p.copy()
        p[1:-1, 1:-1] = (((pd[1:-1, 2:] + pd[1:-1, :-2]) * dy**2 +
                          (pd[2:, 1:-1] + pd[:-2, 1:-1]) * dx**2 -
                          b[1:-1, 1:-1] * dx**2 * dy**2) /
                         (2 * (dx**2 + dy**2)))
        
        # Boundary conditions
        p[0, :] = 0.0
        p[-1, :] = 0.0
        p[:, 0] = 0.0
        p[:, -1] = 0.0
    
    return {
        'x': x,
        'y': y,
        'p': p,
        'b': b,
        'dx': dx,
        'dy': dy,
        'iterations': nt
    }


def cavity_flow_navier_stokes(
    nx: int = 41,
    ny: int = 41,
    nt: int = 500,
    nit: int = 50,
    rho: float = 1.0,
    nu: float = 0.1,
    dt: float = 0.001,
    domain_x: Tuple[float, float] = (0.0, 2.0),
    domain_y: Tuple[float, float] = (0.0, 2.0)
) -> Dict[str, np.ndarray]:
    """
    Solve 2D cavity flow (driven lid) using Navier-Stokes equations.
    
    Parameters
    ----------
    nx, ny : int
        Number of spatial grid points
    nt : int
        Number of time steps
    nit : int
        Number of pressure iterations per time step
    rho : float
        Density
    nu : float
        Dynamic viscosity
    dt : float
        Time step
    domain_x, domain_y : Tuple[float, float]
        Domain bounds
        
    Returns
    -------
    Dict[str, np.ndarray]
        'x': x grid points
        'y': y grid points
        'u': final u velocity
        'v': final v velocity
        'p': final pressure
        'u_history': velocity history
        'p_history': pressure history
    """
    dx = (domain_x[1] - domain_x[0]) / (nx - 1)
    dy = (domain_y[1] - domain_y[0]) / (ny - 1)
    
    x = np.linspace(domain_x[0], domain_x[1], nx)
    y = np.linspace(domain_y[0], domain_y[1], ny)
    
    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.zeros((ny, nx))
    b = np.zeros((ny, nx))
    
    u_history = np.zeros((nt + 1, ny, nx))
    p_history = np.zeros((nt + 1, ny, nx))
    u_history[0, :, :] = u
    p_history[0, :, :] = p
    
    # Time stepping
    for n in range(nt):
        un = u.copy()
        vn = v.copy()
        
        # Build up b for pressure Poisson
        b[1:-1, 1:-1] = (rho * (1 / dt *
                        ((u[1:-1, 2:] - u[1:-1, :-2]) / (2*dx) +
                         (v[2:, 1:-1] - v[:-2, 1:-1]) / (2*dy)) -
                        ((u[1:-1, 2:] - u[1:-1, :-2]) / (2*dx))**2 -
                        2 * ((u[2:, 1:-1] - u[:-2, 1:-1]) / (2*dy) *
                             (v[1:-1, 2:] - v[1:-1, :-2]) / (2*dx)) -
                        ((v[2:, 1:-1] - v[:-2, 1:-1]) / (2*dy))**2))
        
        # Solve pressure Poisson
        pn = p.copy()
        for q in range(nit):
            pn = p.copy()
            p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, :-2]) * dy**2 +
                              (pn[2:, 1:-1] + pn[:-2, 1:-1]) * dx**2) /
                             (2 * (dx**2 + dy**2)) -
                             dx**2 * dy**2 / (2 * (dx**2 + dy**2)) *
                             b[1:-1, 1:-1])
            
            # Pressure boundary conditions
            p[:, -1] = p[:, -2]
            p[0, :] = p[1, :]
            p[:, 0] = p[:, 1]
            p[-1, :] = 0.0
        
        # Solve u momentum
        u[1:-1, 1:-1] = (un[1:-1, 1:-1] -
                         un[1:-1, 1:-1] * dt / dx * (un[1:-1, 1:-1] - un[1:-1, :-2]) -
                         vn[1:-1, 1:-1] * dt / dy * (un[1:-1, 1:-1] - un[:-2, 1:-1]) -
                         dt / (2 * rho * dx) * (p[1:-1, 2:] - p[1:-1, :-2]) +
                         nu * (dt / dx**2 * (un[1:-1, 2:] - 2*un[1:-1, 1:-1] + un[1:-1, :-2]) +
                               dt / dy**2 * (un[2:, 1:-1] - 2*un[1:-1, 1:-1] + un[:-2, 1:-1])))
        
        # Solve v momentum
        v[1:-1, 1:-1] = (vn[1:-1, 1:-1] -
                         un[1:-1, 1:-1] * dt / dx * (vn[1:-1, 1:-1] - vn[1:-1, :-2]) -
                         vn[1:-1, 1:-1] * dt / dy * (vn[1:-1, 1:-1] - vn[:-2, 1:-1]) -
                         dt / (2 * rho * dy) * (p[2:, 1:-1] - p[:-2, 1:-1]) +
                         nu * (dt / dx**2 * (vn[1:-1, 2:] - 2*vn[1:-1, 1:-1] + vn[1:-1, :-2]) +
                               dt / dy**2 * (vn[2:, 1:-1] - 2*vn[1:-1, 1:-1] + vn[:-2, 1:-1])))
        
        # Boundary conditions
        u[0, :] = 0.0
        u[:, 0] = 0.0
        u[:, -1] = 0.0
        u[-1, :] = 1.0  # Moving lid
        
        v[0, :] = 0.0
        v[-1, :] = 0.0
        v[:, 0] = 0.0
        v[:, -1] = 0.0
        
        u_history[n + 1, :, :] = u
        p_history[n + 1, :, :] = p
    
    return {
        'x': x,
        'y': y,
        'u': u,
        'v': v,
        'p': p,
        'u_history': u_history,
        'p_history': p_history,
        'dx': dx,
        'dy': dy,
        'dt': dt,
        't_final': nt * dt,
        'rho': rho,
        'nu': nu
    }
