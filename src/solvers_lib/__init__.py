"""
Reusable numerical PDE solver library for cavity flow and wave equations.
This module provides core computational functions without plotting dependencies.
"""

from .utils import (
    create_1d_grid,
    create_2d_grid,
    create_hat_initial_condition_1d,
    create_hat_initial_condition_2d,
    apply_boundary_conditions_1d,
    apply_boundary_conditions_2d,
)

from .solvers_1d import (
    linear_convection_1d,
    diffusion_1d,
    nonlinear_convection_1d,
    burgers_1d,
)

from .solvers_2d import (
    linear_convection_2d,
    nonlinear_convection_2d,
    diffusion_2d,
    laplace_2d,
    poisson_2d,
    cavity_flow_navier_stokes,
)

from .config import SolverConfig

__all__ = [
    # Utilities
    "create_1d_grid",
    "create_2d_grid",
    "create_hat_initial_condition_1d",
    "create_hat_initial_condition_2d",
    "apply_boundary_conditions_1d",
    "apply_boundary_conditions_2d",
    # 1D Solvers
    "linear_convection_1d",
    "diffusion_1d",
    "nonlinear_convection_1d",
    "burgers_1d",
    # 2D Solvers
    "linear_convection_2d",
    "nonlinear_convection_2d",
    "diffusion_2d",
    "laplace_2d",
    "poisson_2d",
    "cavity_flow_navier_stokes",
    # Configuration
    "SolverConfig",
]
