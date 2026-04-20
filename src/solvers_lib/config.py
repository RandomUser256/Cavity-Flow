"""
Configuration management for solvers.
This module provides classes to manage solver parameters and presets.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class SolverConfig:
    """
    Configuration container for solver parameters.
    Can be easily serialized to JSON for web app usage.
    """
    
    # Spatial discretization
    nx: int = 41
    ny: int = 41
    domain_x_start: float = 0.0
    domain_x_end: float = 2.0
    domain_y_start: float = 0.0
    domain_y_end: float = 2.0
    
    # Temporal discretization
    nt: int = 20
    dt: Optional[float] = None
    
    # Physical parameters
    c: float = 1.0          # Wave speed / advection coefficient
    nu: float = 0.3         # Viscosity / diffusion coefficient
    rho: float = 1.0        # Density (for Navier-Stokes)
    sigma: float = 0.5      # CFL coefficient
    
    # Solver-specific parameters
    nit: int = 50           # Pressure iterations (for Navier-Stokes)
    max_iterations: int = 10000  # Convergence iterations
    tolerance: float = 1e-4  # Convergence tolerance
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for JSON serialization."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert config to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SolverConfig':
        """Create config from dictionary."""
        # Only use valid field names
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'SolverConfig':
        """Create config from JSON string."""
        return cls.from_dict(json.loads(json_str))
    
    @staticmethod
    def preset_linear_convection_1d() -> 'SolverConfig':
        """Preset for 1D linear convection."""
        return SolverConfig(
            nx=41,
            nt=20,
            c=1.0,
            sigma=0.5,
            domain_x_start=0.0,
            domain_x_end=2.0
        )
    
    @staticmethod
    def preset_diffusion_1d() -> 'SolverConfig':
        """Preset for 1D diffusion."""
        return SolverConfig(
            nx=41,
            nt=20,
            nu=0.3,
            sigma=0.2,
            domain_x_start=0.0,
            domain_x_end=2.0
        )
    
    @staticmethod
    def preset_nonlinear_convection_1d() -> 'SolverConfig':
        """Preset for 1D nonlinear convection."""
        return SolverConfig(
            nx=41,
            nt=20,
            dt=0.025,
            domain_x_start=0.0,
            domain_x_end=2.0
        )
    
    @staticmethod
    def preset_burgers_1d() -> 'SolverConfig':
        """Preset for 1D Burgers equation."""
        return SolverConfig(
            nx=101,
            nt=100,
            nu=0.07,
            domain_x_start=0.0,
            domain_x_end=2.0 * 3.141592653589793
        )
    
    @staticmethod
    def preset_linear_convection_2d() -> 'SolverConfig':
        """Preset for 2D linear convection."""
        return SolverConfig(
            nx=101,
            ny=101,
            nt=80,
            c=1.0,
            sigma=0.2,
            domain_x_start=0.0,
            domain_x_end=2.0,
            domain_y_start=0.0,
            domain_y_end=2.0
        )
    
    @staticmethod
    def preset_diffusion_2d() -> 'SolverConfig':
        """Preset for 2D diffusion."""
        return SolverConfig(
            nx=31,
            ny=31,
            nt=17,
            nu=0.05,
            sigma=0.25,
            domain_x_start=0.0,
            domain_x_end=2.0,
            domain_y_start=0.0,
            domain_y_end=2.0
        )
    
    @staticmethod
    def preset_laplace_2d() -> 'SolverConfig':
        """Preset for 2D Laplace equation."""
        return SolverConfig(
            nx=31,
            ny=31,
            tolerance=1e-4,
            max_iterations=10000,
            domain_x_start=0.0,
            domain_x_end=2.0,
            domain_y_start=0.0,
            domain_y_end=1.0
        )
    
    @staticmethod
    def preset_poisson_2d() -> 'SolverConfig':
        """Preset for 2D Poisson equation."""
        return SolverConfig(
            nx=50,
            ny=50,
            nt=100,
            domain_x_start=0.0,
            domain_x_end=2.0,
            domain_y_start=0.0,
            domain_y_end=1.0
        )
    
    @staticmethod
    def preset_cavity_flow() -> 'SolverConfig':
        """Preset for cavity flow (Navier-Stokes)."""
        return SolverConfig(
            nx=41,
            ny=41,
            nt=500,
            nit=50,
            rho=1.0,
            nu=0.1,
            dt=0.001,
            domain_x_start=0.0,
            domain_x_end=2.0,
            domain_y_start=0.0,
            domain_y_end=2.0
        )
    
    @staticmethod
    def preset_cavity_flow_coarse() -> 'SolverConfig':
        """Preset for cavity flow with coarse grid (faster computation)."""
        return SolverConfig(
            nx=21,
            ny=21,
            nt=100,
            nit=30,
            rho=1.0,
            nu=0.1,
            dt=0.001,
            domain_x_start=0.0,
            domain_x_end=2.0,
            domain_y_start=0.0,
            domain_y_end=2.0
        )
    
    @staticmethod
    def get_all_presets() -> Dict[str, callable]:
        """Get all available presets."""
        return {
            'linear_convection_1d': SolverConfig.preset_linear_convection_1d,
            'diffusion_1d': SolverConfig.preset_diffusion_1d,
            'nonlinear_convection_1d': SolverConfig.preset_nonlinear_convection_1d,
            'burgers_1d': SolverConfig.preset_burgers_1d,
            'linear_convection_2d': SolverConfig.preset_linear_convection_2d,
            'diffusion_2d': SolverConfig.preset_diffusion_2d,
            'laplace_2d': SolverConfig.preset_laplace_2d,
            'poisson_2d': SolverConfig.preset_poisson_2d,
            'cavity_flow': SolverConfig.preset_cavity_flow,
            'cavity_flow_coarse': SolverConfig.preset_cavity_flow_coarse,
        }
    
    @classmethod
    def load_preset(cls, preset_name: str) -> 'SolverConfig':
        """Load a preset by name."""
        presets = cls.get_all_presets()
        if preset_name not in presets:
            raise ValueError(f"Unknown preset: {preset_name}. Available: {list(presets.keys())}")
        return presets[preset_name]()
