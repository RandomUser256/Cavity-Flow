"""
Utility functions for grid generation, initial conditions, and boundary conditions.
"""

import numpy as np
from typing import Tuple


def create_1d_grid(domain_start: float, domain_end: float, nx: int) -> np.ndarray:
    """
    Create a 1D uniform grid.
    
    Parameters
    ----------
    domain_start : float
        Start of domain
    domain_end : float
        End of domain
    nx : int
        Number of grid points
        
    Returns
    -------
    np.ndarray
        1D array of grid points
    """
    return np.linspace(domain_start, domain_end, nx)


def create_2d_grid(
    x_start: float, x_end: float, nx: int,
    y_start: float, y_end: float, ny: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Create a 2D uniform grid.
    
    Parameters
    ----------
    x_start, x_end : float
        X domain bounds
    nx : int
        Number of x grid points
    y_start, y_end : float
        Y domain bounds
    ny : int
        Number of y grid points
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
        x, y, X (meshgrid), Y (meshgrid)
    """
    x = np.linspace(x_start, x_end, nx)
    y = np.linspace(y_start, y_end, ny)
    X, Y = np.meshgrid(x, y)
    return x, y, X, Y


def create_hat_initial_condition_1d(
    nx: int, domain_start: float, domain_end: float,
    hat_start: float, hat_end: float, hat_value: float = 2.0
) -> np.ndarray:
    """
    Create 1D hat function initial condition.
    
    Parameters
    ----------
    nx : int
        Number of grid points
    domain_start, domain_end : float
        Domain bounds
    hat_start, hat_end : float
        Bounds of the hat function
    hat_value : float
        Value inside hat (default 2.0)
        
    Returns
    -------
    np.ndarray
        1D array with initial conditions
    """
    dx = (domain_end - domain_start) / (nx - 1)
    u = np.ones(nx)
    u[int(hat_start / dx):int(hat_end / dx + 1)] = hat_value
    return u


def create_hat_initial_condition_2d(
    ny: int, nx: int,
    x_start: float, x_end: float,
    y_start: float, y_end: float,
    hat_x_start: float, hat_x_end: float,
    hat_y_start: float, hat_y_end: float,
    hat_value: float = 2.0
) -> np.ndarray:
    """
    Create 2D hat function initial condition.
    
    Parameters
    ----------
    ny, nx : int
        Grid dimensions
    x_start, x_end : float
        X domain bounds
    y_start, y_end : float
        Y domain bounds
    hat_x_start, hat_x_end : float
        X bounds of the hat
    hat_y_start, hat_y_end : float
        Y bounds of the hat
    hat_value : float
        Value inside hat (default 2.0)
        
    Returns
    -------
    np.ndarray
        2D array with initial conditions
    """
    dx = (x_end - x_start) / (nx - 1)
    dy = (y_end - y_start) / (ny - 1)
    
    u = np.ones((ny, nx))
    u[int(hat_y_start / dy):int(hat_y_end / dy + 1),
      int(hat_x_start / dx):int(hat_x_end / dx + 1)] = hat_value
    return u


def apply_boundary_conditions_1d(
    u: np.ndarray, bc_type: str = "dirichlet", value: float = 1.0
) -> np.ndarray:
    """
    Apply boundary conditions to 1D array.
    
    Parameters
    ----------
    u : np.ndarray
        1D solution array
    bc_type : str
        Type: 'dirichlet', 'periodic', 'neumann'
    value : float
        Boundary value for Dirichlet BC
        
    Returns
    -------
    np.ndarray
        Array with boundary conditions applied
    """
    if bc_type == "dirichlet":
        u[0] = value
        u[-1] = value
    elif bc_type == "periodic":
        # Periodic: no modification needed at boundaries
        pass
    elif bc_type == "neumann":
        # Neumann: zero gradient at boundaries (u'(0) = u'(L) = 0)
        pass
    
    return u


def apply_boundary_conditions_2d(
    u: np.ndarray,
    bc_type: str = "dirichlet_walls",
    wall_value: float = 1.0,
    moving_wall: bool = False,
    moving_wall_value: float = 1.0
) -> np.ndarray:
    """
    Apply boundary conditions to 2D array.
    
    Parameters
    ----------
    u : np.ndarray
        2D solution array (ny x nx)
    bc_type : str
        Type: 'dirichlet_walls', 'cavity_flow', 'periodic'
    wall_value : float
        Value at walls
    moving_wall : bool
        Whether to apply moving wall (for cavity flow)
    moving_wall_value : float
        Value of moving wall velocity
        
    Returns
    -------
    np.ndarray
        Array with boundary conditions applied
    """
    if bc_type == "dirichlet_walls":
        u[0, :] = wall_value   # bottom
        u[-1, :] = wall_value  # top
        u[:, 0] = wall_value   # left
        u[:, -1] = wall_value  # right
    
    elif bc_type == "cavity_flow":
        u[0, :] = wall_value   # bottom
        u[:, 0] = wall_value   # left
        u[:, -1] = wall_value  # right
        if moving_wall:
            u[-1, :] = moving_wall_value  # top (moving wall)
        else:
            u[-1, :] = wall_value
    
    elif bc_type == "periodic":
        # Periodic boundary conditions handled elsewhere
        pass
    
    return u


def get_grid_spacing(domain_start: float, domain_end: float, num_points: int) -> float:
    """
    Calculate grid spacing.
    
    Parameters
    ----------
    domain_start, domain_end : float
        Domain bounds
    num_points : int
        Number of grid points
        
    Returns
    -------
    float
        Grid spacing (dx or dy)
    """
    return (domain_end - domain_start) / (num_points - 1)


def calculate_courant_number(dt: float, dx: float, c: float) -> float:
    """
    Calculate Courant number (CFL condition).
    
    Parameters
    ----------
    dt : float
        Time step
    dx : float
        Grid spacing
    c : float
        Wave speed
        
    Returns
    -------
    float
        Courant number (should be <= 1 for stability)
    """
    return c * dt / dx


def stable_dt_from_sigma(sigma: float, dx: float, c: float = 1.0) -> float:
    """
    Calculate stable time step from sigma parameter.
    
    Parameters
    ----------
    sigma : float
        CFL coefficient (typically 0.5 for advection)
    dx : float
        Grid spacing
    c : float
        Wave speed
        
    Returns
    -------
    float
        Time step dt
    """
    return sigma * dx / c
