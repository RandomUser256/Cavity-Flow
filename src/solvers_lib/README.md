# Solvers Library - Refactored CFD/PDE Solvers

A modular, reusable library for numerical solving of PDEs using finite difference methods. Designed for easy web app integration without plotting dependencies.

## Features

- **1D Solvers**: Linear convection, Diffusion, Nonlinear convection, Burgers' equation
- **2D Solvers**: Linear/Nonlinear convection, Diffusion, Laplace, Poisson, Cavity flow (Navier-Stokes)
- **Modular Design**: Separate concerns for grid generation, boundary conditions, and solvers
- **JSON-Friendly**: Built-in serialization for web APIs
- **Configuration Management**: Presets and parameter management
- **Web Integration**: Flask example app included
- **No Plotting Dependencies**: Pure computational functions

## Installation

```bash
# Copy solvers_lib to your project
cp -r solvers_lib/ /path/to/your/project/

# Install dependencies
pip install numpy flask flask-cors
```

## Quick Start

### Basic Usage

```python
from solvers_lib import linear_convection_1d, cavity_flow_navier_stokes
from solvers_lib.config import SolverConfig

# Using default parameters
result = linear_convection_1d()
print(result['u'])  # Final solution
print(result['x'])  # Grid points

# Using custom parameters
result = linear_convection_1d(
    nx=51,
    nt=30,
    c=1.0,
    sigma=0.5
)

# Using presets
config = SolverConfig.preset_cavity_flow()
result = cavity_flow_navier_stokes(**config.__dict__)
```

### Web API Usage

```python
from solvers_lib.web_api import WebSolverAPI
from solvers_lib.config import SolverConfig

# Run solver with preset
result = WebSolverAPI.solve('linear_convection_1d')

# Run solver with custom config
config = {
    'nx': 51,
    'nt': 30,
    'c': 1.0,
    'sigma': 0.5
}
result = WebSolverAPI.solve('linear_convection_1d', config)

# Get available solvers
solvers = WebSolverAPI.get_available_solvers()
```

### Flask Web App

```bash
# Run the Flask app
cd src
python flask_app.py
```

API Endpoints:
- `GET /api/health` - Health check
- `GET /api/solvers` - List available solvers
- `GET /api/presets` - List available presets
- `GET /api/preset/<preset_name>` - Get preset configuration
- `POST /api/solve` - Run solver
- `GET/POST /api/solve/<solver_name>` - Run specific solver

#### Example Requests

```bash
# Run solver with preset
curl -X GET http://localhost:5000/api/solve/linear_convection_1d

# Run solver with custom config
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "solver_name": "linear_convection_1d",
    "config": {
      "nx": 51,
      "nt": 30,
      "c": 1.0,
      "sigma": 0.5
    }
  }'
```

## Library Structure

```
solvers_lib/
├── __init__.py              # Package initialization and exports
├── utils.py                 # Grid generation, initial conditions, BC
├── solvers_1d.py            # 1D solver functions
├── solvers_2d.py            # 2D solver functions
├── config.py                # Configuration management
└── web_api.py               # Web API wrapper
```

## Available Solvers

### 1D Solvers

#### `linear_convection_1d(nx, nt, domain_start, domain_end, c, sigma, initial_condition)`
Solves: `∂u/∂t + c·∂u/∂x = 0`

#### `diffusion_1d(nx, nt, domain_start, domain_end, nu, sigma, initial_condition)`
Solves: `∂u/∂t = ν·∂²u/∂x²`

#### `nonlinear_convection_1d(nx, nt, domain_start, domain_end, dt, initial_condition)`
Solves: `∂u/∂t + u·∂u/∂x = 0`

#### `burgers_1d(nx, nt, domain_start, domain_end, nu, dt, use_analytical)`
Solves: `∂u/∂t + u·∂u/∂x = ν·∂²u/∂x²`

### 2D Solvers

#### `linear_convection_2d(nx, ny, nt, domain_x, domain_y, c, sigma, initial_condition)`
Solves: `∂u/∂t + c·(∂u/∂x + ∂u/∂y) = 0`

#### `nonlinear_convection_2d(nx, ny, nt, domain_x, domain_y, c, sigma, initial_condition)`
Solves: `∂u/∂t + u·∂u/∂x + v·∂u/∂y = 0`

#### `diffusion_2d(nx, ny, nt, domain_x, domain_y, nu, sigma, initial_condition)`
Solves: `∂u/∂t = ν·(∂²u/∂x² + ∂²u/∂y²)`

#### `laplace_2d(nx, ny, domain_x, domain_y, l1norm_target, max_iterations)`
Solves: `∇²p = 0` (iterative)

#### `poisson_2d(nx, ny, nt, domain_x, domain_y, source_term)`
Solves: `∇²p = b` (iterative)

#### `cavity_flow_navier_stokes(nx, ny, nt, nit, rho, nu, dt, domain_x, domain_y)`
Solves 2D Navier-Stokes in a driven cavity

## Output Format

All solvers return a dictionary with:

```python
{
    'x': np.ndarray,           # x grid points (1D) or (2D)
    'y': np.ndarray,           # y grid points (2D only)
    'u': np.ndarray,           # solution field
    'history': np.ndarray,     # solution history (optional)
    'dx': float,               # grid spacing
    'dy': float,               # grid spacing (2D)
    'dt': float,               # time step
    't_final': float,          # final time
    # ... solver-specific parameters
}
```

## Configuration Presets

Available presets:
- `linear_convection_1d`
- `diffusion_1d`
- `nonlinear_convection_1d`
- `burgers_1d`
- `linear_convection_2d`
- `diffusion_2d`
- `laplace_2d`
- `poisson_2d`
- `cavity_flow`
- `cavity_flow_coarse`

```python
from solvers_lib.config import SolverConfig

# Load preset
config = SolverConfig.load_preset('cavity_flow')

# Convert to dictionary/JSON
config_dict = config.to_dict()
config_json = config.to_json()

# Create from dictionary
config = SolverConfig.from_dict({'nx': 41, 'nt': 20})
```

## Advanced Usage

### Custom Initial Conditions

```python
import numpy as np
from solvers_lib.utils import create_1d_grid
from solvers_lib import linear_convection_1d

# Create custom IC
x = create_1d_grid(0, 2, 41)
custom_ic = np.sin(np.pi * x)

# Use with solver
result = linear_convection_1d(
    nx=41,
    nt=20,
    initial_condition=custom_ic
)
```

### Batch Processing

```python
from solvers_lib.web_api import WebSolverAPI
from solvers_lib.config import SolverConfig

# Run multiple solvers
solvers = ['linear_convection_1d', 'diffusion_1d', 'nonlinear_convection_1d']

results = {}
for solver_name in solvers:
    results[solver_name] = WebSolverAPI.solve(solver_name)
```

### JSON Serialization

```python
import json
from solvers_lib.web_api import NumpyJSONEncoder, serialize_result

result = linear_convection_1d()

# Serialize with custom encoder
json_str = json.dumps(result, cls=NumpyJSONEncoder)

# Or use convenience function
json_str = serialize_result(result, include_history=True)
```

## Performance Considerations

- **Coarse grids** (nx=21) for fast iteration/testing
- **Fine grids** (nx=101+) for accuracy
- **Time steps**: smaller for stability, larger for speed
- **Iterations**: Use fewer for 2D elliptic solvers for quick results

For large problems, consider:
- Reducing `nt` (time steps)
- Using coarser grids
- Implementing parallel computation

## Integration with Existing Code

The library is backward compatible with existing scripts. You can:

1. Import individual solvers:
```python
from solvers_lib.solvers_1d import linear_convection_1d
```

2. Use as drop-in replacement for old scripts
3. Gradually refactor existing code

## Troubleshooting

**Issue**: Solver diverges
- Reduce `dt` or increase `sigma`
- Check CFL condition: `c*dt/dx <= sigma`

**Issue**: Slow convergence (iterative solvers)
- Reduce tolerance (`tolerance` parameter)
- Increase max iterations
- Use coarser initial grid

**Issue**: Memory issues with large arrays
- Reduce grid size (nx, ny)
- Disable history (`include_history=False`)

## References

The solvers implement standard finite difference methods for:
- Linear advection equations
- Diffusion/Heat equations
- Nonlinear convection
- Burgers' equation
- Laplace/Poisson equations
- Navier-Stokes equations

## License

Same as parent project

## Future Enhancements

- GPU acceleration (CuPy)
- Implicit time stepping
- Adaptive mesh refinement
- Higher-order schemes
- Parallel computation
