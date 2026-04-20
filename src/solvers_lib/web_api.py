"""
Web API wrapper for solvers.
Provides convenient functions for web app integration with JSON serialization.
"""

import json
import numpy as np
from typing import Dict, Any, Optional
from .solvers_1d import (
    linear_convection_1d,
    diffusion_1d,
    nonlinear_convection_1d,
    burgers_1d
)
from .solvers_2d import (
    linear_convection_2d,
    nonlinear_convection_2d,
    diffusion_2d,
    laplace_2d,
    poisson_2d,
    cavity_flow_navier_stokes
)
from .config import SolverConfig


class NumpyJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy arrays."""
    
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        return super().default(obj)


def serialize_result(result: Dict[str, Any], include_history: bool = False) -> str:
    """
    Serialize solver result to JSON.
    
    Parameters
    ----------
    result : Dict[str, np.ndarray]
        Solver result dictionary
    include_history : bool
        Whether to include solution history
        
    Returns
    -------
    str
        JSON string
    """
    # Create a copy to avoid modifying original
    output = {}
    for key, value in result.items():
        if key == 'history' and not include_history:
            continue
        output[key] = value
    
    return json.dumps(output, cls=NumpyJSONEncoder)


class WebSolverAPI:
    """
    Web-friendly wrapper for all solvers.
    Handles parameter validation and JSON serialization.
    """
    
    SOLVERS_1D = {
        'linear_convection_1d': linear_convection_1d,
        'diffusion_1d': diffusion_1d,
        'nonlinear_convection_1d': nonlinear_convection_1d,
        'burgers_1d': burgers_1d,
    }
    
    SOLVERS_2D = {
        'linear_convection_2d': linear_convection_2d,
        'nonlinear_convection_2d': nonlinear_convection_2d,
        'diffusion_2d': diffusion_2d,
        'laplace_2d': laplace_2d,
        'poisson_2d': poisson_2d,
        'cavity_flow_navier_stokes': cavity_flow_navier_stokes,
    }
    
    @staticmethod
    def get_available_solvers() -> Dict[str, list]:
        """Get list of available solvers."""
        return {
            '1d_solvers': list(WebSolverAPI.SOLVERS_1D.keys()),
            '2d_solvers': list(WebSolverAPI.SOLVERS_2D.keys()),
        }
    
    @staticmethod
    def solve(
        solver_name: str,
        config: Optional[Dict[str, Any]] = None,
        include_history: bool = False
    ) -> Dict[str, Any]:
        """
        Run a solver with given configuration.
        
        Parameters
        ----------
        solver_name : str
            Name of the solver to run
        config : Dict[str, Any], optional
            Configuration dictionary. If None, uses default preset.
        include_history : bool
            Whether to include solution history in output
            
        Returns
        -------
        Dict[str, Any]
            Solver result (numpy arrays converted to lists)
        """
        # Get solver
        all_solvers = {**WebSolverAPI.SOLVERS_1D, **WebSolverAPI.SOLVERS_2D}
        if solver_name not in all_solvers:
            raise ValueError(f"Unknown solver: {solver_name}")
        
        solver_func = all_solvers[solver_name]
        
        # Load or create configuration
        if config is None:
            # Try to load default preset
            try:
                cfg = SolverConfig.load_preset(solver_name)
            except ValueError:
                cfg = SolverConfig()
        else:
            cfg = SolverConfig.from_dict(config)
        
        # Extract parameters for the specific solver
        kwargs = WebSolverAPI._prepare_solver_kwargs(solver_name, cfg)
        
        # Run solver
        result = solver_func(**kwargs)
        
        # Prepare output
        output = {}
        for key, value in result.items():
            if key == 'history' and not include_history:
                continue
            elif isinstance(value, np.ndarray):
                output[key] = value.tolist()
            else:
                output[key] = value
        
        output['solver_name'] = solver_name
        output['config'] = cfg.to_dict()
        
        return output
    
    @staticmethod
    def _prepare_solver_kwargs(solver_name: str, config: SolverConfig) -> Dict[str, Any]:
        """Prepare kwargs for specific solver."""
        kwargs = {}
        
        if solver_name in ['linear_convection_1d', 'diffusion_1d', 'nonlinear_convection_1d']:
            kwargs['nx'] = config.nx
            kwargs['nt'] = config.nt
            kwargs['domain_start'] = config.domain_x_start
            kwargs['domain_end'] = config.domain_x_end
        
        if solver_name == 'linear_convection_1d':
            kwargs['c'] = config.c
            kwargs['sigma'] = config.sigma
        
        elif solver_name == 'diffusion_1d':
            kwargs['nu'] = config.nu
            kwargs['sigma'] = config.sigma
        
        elif solver_name == 'nonlinear_convection_1d':
            kwargs['dt'] = config.dt or 0.025
        
        elif solver_name == 'burgers_1d':
            kwargs['nx'] = config.nx
            kwargs['nt'] = config.nt
            kwargs['domain_start'] = config.domain_x_start
            kwargs['domain_end'] = config.domain_x_end
            kwargs['nu'] = config.nu
            kwargs['dt'] = config.dt
            kwargs['use_analytical'] = True
        
        elif solver_name in ['linear_convection_2d', 'nonlinear_convection_2d', 'diffusion_2d']:
            kwargs['nx'] = config.nx
            kwargs['ny'] = config.ny
            kwargs['nt'] = config.nt
            kwargs['domain_x'] = (config.domain_x_start, config.domain_x_end)
            kwargs['domain_y'] = (config.domain_y_start, config.domain_y_end)
        
        if solver_name == 'linear_convection_2d':
            kwargs['c'] = config.c
            kwargs['sigma'] = config.sigma
        
        elif solver_name == 'nonlinear_convection_2d':
            kwargs['c'] = config.c
            kwargs['sigma'] = config.sigma
        
        elif solver_name == 'diffusion_2d':
            kwargs['nu'] = config.nu
            kwargs['sigma'] = config.sigma
        
        elif solver_name == 'laplace_2d':
            kwargs['nx'] = config.nx
            kwargs['ny'] = config.ny
            kwargs['domain_x'] = (config.domain_x_start, config.domain_x_end)
            kwargs['domain_y'] = (config.domain_y_start, config.domain_y_end)
            kwargs['l1norm_target'] = config.tolerance
            kwargs['max_iterations'] = config.max_iterations
        
        elif solver_name == 'poisson_2d':
            kwargs['nx'] = config.nx
            kwargs['ny'] = config.ny
            kwargs['nt'] = config.nt
            kwargs['domain_x'] = (config.domain_x_start, config.domain_x_end)
            kwargs['domain_y'] = (config.domain_y_start, config.domain_y_end)
        
        elif solver_name == 'cavity_flow_navier_stokes':
            kwargs['nx'] = config.nx
            kwargs['ny'] = config.ny
            kwargs['nt'] = config.nt
            kwargs['nit'] = config.nit
            kwargs['rho'] = config.rho
            kwargs['nu'] = config.nu
            kwargs['dt'] = config.dt or 0.001
            kwargs['domain_x'] = (config.domain_x_start, config.domain_x_end)
            kwargs['domain_y'] = (config.domain_y_start, config.domain_y_end)
        
        return kwargs
    
    @staticmethod
    def solve_with_json(json_request: str, include_history: bool = False) -> str:
        """
        Solve from JSON request and return JSON response.
        
        JSON request format:
        {
            "solver_name": "linear_convection_1d",
            "config": {
                "nx": 41,
                "nt": 20,
                ...
            }
        }
        
        Parameters
        ----------
        json_request : str
            JSON request string
        include_history : bool
            Whether to include history
            
        Returns
        -------
        str
            JSON response
        """
        request = json.loads(json_request)
        solver_name = request['solver_name']
        config = request.get('config')
        
        result = WebSolverAPI.solve(solver_name, config, include_history)
        return json.dumps(result, cls=NumpyJSONEncoder)


# Convenience functions for common use cases
def solve_1d(solver_name: str, **kwargs) -> Dict[str, Any]:
    """Solve a 1D problem."""
    return WebSolverAPI.SOLVERS_1D[solver_name](**kwargs)


def solve_2d(solver_name: str, **kwargs) -> Dict[str, Any]:
    """Solve a 2D problem."""
    return WebSolverAPI.SOLVERS_2D[solver_name](**kwargs)
