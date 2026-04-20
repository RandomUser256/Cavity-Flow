"""
1D numerical solvers for various PDEs.
Functions return numerical solutions as numpy arrays without plotting.
"""

import numpy as np
from typing import Tuple, Dict
from .utils import apply_boundary_conditions_1d


def linear_convection_1d(
    nx: int = 41,
    nt: int = 20,
    domain_start: float = 0.0,
    domain_end: float = 2.0,
    c: float = 1.0,
    sigma: float = 0.5,
    initial_condition: np.ndarray = None
) -> Dict[str, np.ndarray]:
    """
    Solve 1D linear convection equation: du/dt + c*du/dx = 0
    
    Parameters
    ----------
    nx : int
        Number of spatial grid points
    nt : int
        Number of time steps
    domain_start, domain_end : float
        Domain bounds
    c : float
        Wave speed
    sigma : float
        CFL coefficient (for stability: c*dt/dx <= sigma)
    initial_condition : np.ndarray, optional
        Custom initial condition. If None, uses hat function
        
    Returns
    -------
    Dict[str, np.ndarray]
        'x': grid points
        'u': final solution
        'history': solution history at all time steps
    """
    dx = (domain_end - domain_start) / (nx - 1)
    dt = sigma * dx / c
    x = np.linspace(domain_start, domain_end, nx)
    
    # Initialize solution
    if initial_condition is None:
        u = np.ones(nx)
        u[int(0.5 / dx):int(1.0 / dx + 1)] = 2.0
    else:
        u = initial_condition.copy()
    
    un = np.ones(nx)
    history = np.zeros((nt + 1, nx))
    history[0, :] = u
    
    # Time stepping
    for n in range(nt):
        un = u.copy()
        for i in range(1, nx):
            u[i] = un[i] - c * dt / dx * (un[i] - un[i-1])
        history[n + 1, :] = u
    
    return {
        'x': x,
        'u': u,
        'history': history,
        'dx': dx,
        'dt': dt,
        't_final': nt * dt
    }


def diffusion_1d(
    nx: int = 41,
    nt: int = 20,
    domain_start: float = 0.0,
    domain_end: float = 2.0,
    nu: float = 0.3,
    sigma: float = 0.2,
    initial_condition: np.ndarray = None
) -> Dict[str, np.ndarray]:
    """
    Solve 1D diffusion (heat) equation: du/dt = nu*d²u/dx²
    
    Parameters
    ----------
    nx : int
        Number of spatial grid points
    nt : int
        Number of time steps
    domain_start, domain_end : float
        Domain bounds
    nu : float
        Diffusion coefficient (viscosity)
    sigma : float
        Stability parameter for time step
    initial_condition : np.ndarray, optional
        Custom initial condition. If None, uses hat function
        
    Returns
    -------
    Dict[str, np.ndarray]
        'x': grid points
        'u': final solution
        'history': solution history
    """
    dx = (domain_end - domain_start) / (nx - 1)
    dt = sigma * dx**2 / nu
    x = np.linspace(domain_start, domain_end, nx)
    
    # Initialize solution
    if initial_condition is None:
        u = np.ones(nx)
        u[int(0.5 / dx):int(1.0 / dx + 1)] = 2.0
    else:
        u = initial_condition.copy()
    
    un = np.ones(nx)
    history = np.zeros((nt + 1, nx))
    history[0, :] = u
    
    # Time stepping
    for n in range(nt):
        un = u.copy()
        for i in range(1, nx - 1):
            u[i] = un[i] + nu * dt / dx**2 * (un[i+1] - 2*un[i] + un[i-1])
        # Boundary conditions
        u[0] = 1.0
        u[-1] = 1.0
        history[n + 1, :] = u
    
    return {
        'x': x,
        'u': u,
        'history': history,
        'dx': dx,
        'dt': dt,
        't_final': nt * dt,
        'nu': nu
    }


def nonlinear_convection_1d(
    nx: int = 41,
    nt: int = 20,
    domain_start: float = 0.0,
    domain_end: float = 2.0,
    dt: float = 0.025,
    initial_condition: np.ndarray = None
) -> Dict[str, np.ndarray]:
    """
    Solve 1D nonlinear convection equation: du/dt + u*du/dx = 0
    
    Parameters
    ----------
    nx : int
        Number of spatial grid points
    nt : int
        Number of time steps
    domain_start, domain_end : float
        Domain bounds
    dt : float
        Time step
    initial_condition : np.ndarray, optional
        Custom initial condition. If None, uses hat function
        
    Returns
    -------
    Dict[str, np.ndarray]
        'x': grid points
        'u': final solution
        'history': solution history
    """
    dx = (domain_end - domain_start) / (nx - 1)
    x = np.linspace(domain_start, domain_end, nx)
    
    # Initialize solution
    if initial_condition is None:
        u = np.ones(nx)
        u[int(0.5 / dx):int(1.0 / dx + 1)] = 2.0
    else:
        u = initial_condition.copy()
    
    un = np.ones(nx)
    history = np.zeros((nt + 1, nx))
    history[0, :] = u
    
    # Time stepping
    for n in range(nt):
        un = u.copy()
        for i in range(1, nx):
            u[i] = un[i] - (un[i] * dt / dx * (un[i] - un[i-1]))
        history[n + 1, :] = u
    
    return {
        'x': x,
        'u': u,
        'history': history,
        'dx': dx,
        'dt': dt,
        't_final': nt * dt
    }


def burgers_1d(
    nx: int = 101,
    nt: int = 100,
    domain_start: float = 0.0,
    domain_end: float = 2.0 * np.pi,
    nu: float = 0.07,
    dt: float = None,
    use_analytical: bool = True
) -> Dict[str, np.ndarray]:
    """
    Solve 1D Burgers' equation: du/dt + u*du/dx = nu*d²u/dx²
    
    This solves the nonlinear version with viscosity.
    Optionally compares with analytical solution.
    
    Parameters
    ----------
    nx : int
        Number of spatial grid points
    nt : int
        Number of time steps
    domain_start, domain_end : float
        Domain bounds
    nu : float
        Viscosity coefficient
    dt : float, optional
        Time step. If None, calculated from dx*nu
    use_analytical : bool
        Whether to compute analytical solution for comparison
        
    Returns
    -------
    Dict[str, np.ndarray]
        'x': grid points
        'u': numerical solution
        'u_analytical': analytical solution (if use_analytical=True)
        'history': solution history
    """
    dx = (domain_end - domain_start) / (nx - 1)
    if dt is None:
        dt = dx * nu
    x = np.linspace(domain_start, domain_end, nx)
    
    # Analytical solution via SymPy (for comparison)
    if use_analytical:
        try:
            import sympy
            from sympy.utilities.lambdify import lambdify
            
            x_sym, nu_sym, t_sym = sympy.symbols('x nu t')
            phi = (sympy.exp(-(x_sym - 4*t_sym)**2 / (4*nu_sym*(t_sym+1))) +
                   sympy.exp(-(x_sym - 4*t_sym - 2*sympy.pi)**2 / (4*nu_sym*(t_sym+1))))
            phiprime = phi.diff(x_sym)
            u_analytical_expr = -2*nu_sym*(phiprime/phi) + 4
            
            ufunc = lambdify((t_sym, x_sym, nu_sym), u_analytical_expr)
            t0 = 0
            u_init = np.array([ufunc(t0, xi, nu) for xi in x])
            u_analytical_final = np.array([ufunc(nt*dt, xi, nu) for xi in x])
        except ImportError:
            use_analytical = False
            u_init = np.ones(nx)
            u_analytical_final = None
    else:
        u_init = np.ones(nx)
        u_analytical_final = None
    
    u = u_init.copy()
    un = np.empty(nx)
    history = np.zeros((nt + 1, nx))
    history[0, :] = u
    
    # Time stepping
    for n in range(nt):
        un = u.copy()
        for i in range(1, nx-1):
            u[i] = (un[i] - un[i] * dt / dx * (un[i] - un[i-1]) +
                    nu * dt / dx**2 * (un[i+1] - 2*un[i] + un[i-1]))
        
        # Periodic boundary conditions
        u[0] = (un[0] - un[0] * dt / dx * (un[0] - un[-2]) +
                nu * dt / dx**2 * (un[1] - 2*un[0] + un[-2]))
        u[-1] = u[0]
        history[n + 1, :] = u
    
    result = {
        'x': x,
        'u': u,
        'history': history,
        'dx': dx,
        'dt': dt,
        't_final': nt * dt,
        'nu': nu
    }
    
    if use_analytical and u_analytical_final is not None:
        result['u_analytical'] = u_analytical_final
    
    return result
