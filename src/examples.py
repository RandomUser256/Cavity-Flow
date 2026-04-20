"""
Example usage of the refactored solvers library.
Demonstrates various use cases and integration patterns.
"""

import json
import numpy as np
from solvers_lib import (
    linear_convection_1d,
    diffusion_1d,
    nonlinear_convection_1d,
    burgers_1d,
    linear_convection_2d,
    nonlinear_convection_2d,
    diffusion_2d,
    laplace_2d,
    poisson_2d,
    cavity_flow_navier_stokes
)
from solvers_lib.config import SolverConfig
from solvers_lib.web_api import WebSolverAPI, NumpyJSONEncoder
from solvers_lib.utils import (
    create_1d_grid,
    create_2d_grid,
    create_hat_initial_condition_1d
)


def example_1d_linear_convection():
    """Example: 1D linear convection with default parameters."""
    print("=" * 60)
    print("Example 1: 1D Linear Convection (Default)")
    print("=" * 60)
    
    result = linear_convection_1d()
    
    print(f"Grid points (nx): {len(result['x'])}")
    print(f"Time steps: {result['t_final'] / result['dt']:.0f}")
    print(f"Final time: {result['t_final']:.4f}")
    print(f"Solution shape: {result['u'].shape}")
    print(f"Solution min/max: {result['u'].min():.4f} / {result['u'].max():.4f}")
    print()


def example_1d_custom_config():
    """Example: 1D linear convection with custom parameters."""
    print("=" * 60)
    print("Example 2: 1D Linear Convection (Custom Config)")
    print("=" * 60)
    
    config = {
        'nx': 81,
        'nt': 40,
        'c': 1.5,
        'sigma': 0.5
    }
    
    result = linear_convection_1d(**config)
    
    print(f"Custom parameters:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print(f"Solution min/max: {result['u'].min():.4f} / {result['u'].max():.4f}")
    print()


def example_1d_with_preset():
    """Example: Using preset configurations."""
    print("=" * 60)
    print("Example 3: Using SolverConfig Presets")
    print("=" * 60)
    
    presets = ['linear_convection_1d', 'diffusion_1d', 'nonlinear_convection_1d', 'burgers_1d']
    
    for preset_name in presets:
        config = SolverConfig.load_preset(preset_name)
        print(f"Preset: {preset_name}")
        print(f"  nx={config.nx}, nt={config.nt}, nu={config.nu}, c={config.c}")
    print()


def example_custom_initial_condition():
    """Example: Custom initial condition."""
    print("=" * 60)
    print("Example 4: Custom Initial Condition")
    print("=" * 60)
    
    nx = 51
    x = create_1d_grid(0, 2, nx)
    
    # Create sine wave initial condition
    custom_ic = 1 + 0.5 * np.sin(np.pi * x)
    
    result = linear_convection_1d(
        nx=nx,
        nt=30,
        initial_condition=custom_ic
    )
    
    print(f"Initial condition: sine wave")
    print(f"IC min/max: {custom_ic.min():.4f} / {custom_ic.max():.4f}")
    print(f"Final solution min/max: {result['u'].min():.4f} / {result['u'].max():.4f}")
    print()


def example_2d_solvers():
    """Example: 2D solvers."""
    print("=" * 60)
    print("Example 5: 2D Solvers")
    print("=" * 60)
    
    # Linear convection 2D
    result_lc = linear_convection_2d(
        nx=51,
        ny=51,
        nt=40
    )
    print(f"Linear Convection 2D:")
    print(f"  Grid: {result_lc['u'].shape}")
    print(f"  u min/max: {result_lc['u'].min():.4f} / {result_lc['u'].max():.4f}")
    
    # Diffusion 2D
    result_diff = diffusion_2d(
        nx=31,
        ny=31,
        nt=15
    )
    print(f"Diffusion 2D:")
    print(f"  Grid: {result_diff['u'].shape}")
    print(f"  u min/max: {result_diff['u'].min():.4f} / {result_diff['u'].max():.4f}")
    print()


def example_elliptic_solvers():
    """Example: Elliptic equation solvers."""
    print("=" * 60)
    print("Example 6: Elliptic Solvers (Laplace & Poisson)")
    print("=" * 60)
    
    # Laplace equation
    result_laplace = laplace_2d(
        nx=31,
        ny=31,
        l1norm_target=1e-4
    )
    print(f"Laplace 2D:")
    print(f"  Iterations: {result_laplace['iterations']}")
    print(f"  Converged: {result_laplace['converged']}")
    print(f"  p min/max: {result_laplace['p'].min():.4f} / {result_laplace['p'].max():.4f}")
    
    # Poisson equation
    result_poisson = poisson_2d(
        nx=40,
        ny=40,
        nt=100
    )
    print(f"Poisson 2D:")
    print(f"  Iterations: {result_poisson['iterations']}")
    print(f"  p min/max: {result_poisson['p'].min():.4f} / {result_poisson['p'].max():.4f}")
    print()


def example_cavity_flow():
    """Example: Cavity flow (Navier-Stokes)."""
    print("=" * 60)
    print("Example 7: Cavity Flow (Navier-Stokes)")
    print("=" * 60)
    
    # Use coarse grid for demo
    result = cavity_flow_navier_stokes(
        nx=21,
        ny=21,
        nt=50,
        nit=20
    )
    
    print(f"Cavity Flow 2D:")
    print(f"  Grid: {result['u'].shape}")
    print(f"  Time steps: {result['nt']}")
    print(f"  Final time: {result['t_final']:.4f}")
    print(f"  u velocity min/max: {result['u'].min():.4f} / {result['u'].max():.4f}")
    print(f"  v velocity min/max: {result['v'].min():.4f} / {result['v'].max():.4f}")
    print(f"  Pressure min/max: {result['p'].min():.4f} / {result['p'].max():.4f}")
    print()


def example_web_api():
    """Example: Using the web API."""
    print("=" * 60)
    print("Example 8: Web API Usage")
    print("=" * 60)
    
    # Get available solvers
    solvers = WebSolverAPI.get_available_solvers()
    print(f"Available solvers:")
    print(f"  1D: {', '.join(solvers['1d_solvers'])}")
    print(f"  2D: {', '.join(solvers['2d_solvers'])}")
    
    # Run solver via web API
    result = WebSolverAPI.solve('linear_convection_1d')
    print(f"\nWeb API result keys: {list(result.keys())}")
    print(f"Solver name: {result['solver_name']}")
    print(f"Solution shape: {np.array(result['u']).shape}")
    print()


def example_json_serialization():
    """Example: JSON serialization."""
    print("=" * 60)
    print("Example 9: JSON Serialization")
    print("=" * 60)
    
    # Run solver
    result = linear_convection_1d(nx=21, nt=10)
    
    # Remove history to keep JSON small
    result_no_history = {k: v for k, v in result.items() if k != 'history'}
    
    # Serialize to JSON
    json_str = json.dumps(result_no_history, cls=NumpyJSONEncoder, indent=2)
    
    print(f"JSON output (first 500 chars):")
    print(json_str[:500])
    print("...")
    print()


def example_batch_processing():
    """Example: Batch processing multiple solvers."""
    print("=" * 60)
    print("Example 10: Batch Processing")
    print("=" * 60)
    
    solvers_to_run = [
        'linear_convection_1d',
        'diffusion_1d',
        'nonlinear_convection_1d'
    ]
    
    results = {}
    for solver_name in solvers_to_run:
        result = WebSolverAPI.solve(solver_name)
        results[solver_name] = {
            'nx': result['config']['nx'],
            'nt': result['config']['nt'],
            'u_max': float(np.array(result['u']).max()),
            'u_min': float(np.array(result['u']).min())
        }
    
    print("Batch processing results:")
    for solver_name, data in results.items():
        print(f"  {solver_name}:")
        print(f"    Grid: {data['nx']}, Time steps: {data['nt']}")
        print(f"    Solution range: [{data['u_min']:.4f}, {data['u_max']:.4f}]")
    print()


def example_config_management():
    """Example: Configuration management."""
    print("=" * 60)
    print("Example 11: Configuration Management")
    print("=" * 60)
    
    # Create config
    config = SolverConfig(
        nx=51,
        nt=30,
        c=1.0,
        sigma=0.5
    )
    
    print(f"Original config:")
    print(f"  {config}")
    
    # Convert to dict and JSON
    config_dict = config.to_dict()
    config_json = config.to_json()
    
    print(f"\nAs dictionary: {list(config_dict.keys())[:5]}...")
    print(f"As JSON (first 200 chars):")
    print(config_json[:200] + "...")
    
    # Recreate from JSON
    config_restored = SolverConfig.from_json(config_json)
    print(f"\nRestored config: nx={config_restored.nx}, nt={config_restored.nt}")
    print()


def main():
    """Run all examples."""
    print("\n")
    print("█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  Solvers Library - Usage Examples".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    print("\n")
    
    example_1d_linear_convection()
    example_1d_custom_config()
    example_1d_with_preset()
    example_custom_initial_condition()
    example_2d_solvers()
    example_elliptic_solvers()
    example_cavity_flow()
    example_web_api()
    example_json_serialization()
    example_batch_processing()
    example_config_management()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print("\nFor more information, see solvers_lib/README.md")


if __name__ == '__main__':
    main()
