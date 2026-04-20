# Quick Start Guide - Solvers Library

Get started with the refactored solvers in 5 minutes.

## Installation

```bash
# Navigate to the project
cd c:\Users\maxim\OneDrive\Documents\GitHub\Cavity-Flow

# Install dependencies
pip install -r src/solvers_lib/requirements.txt
```

## Quick Examples

### 1. Run a Solver (Simplest)

```python
from solvers_lib import linear_convection_1d

result = linear_convection_1d()
print(result['u'])  # Final solution
```

### 2. With Custom Parameters

```python
from solvers_lib import cavity_flow_navier_stokes

result = cavity_flow_navier_stokes(
    nx=41,
    ny=41, 
    nt=100,
    nu=0.1
)

u_velocity = result['u']  # 2D velocity field
pressure = result['p']    # 2D pressure field
```

### 3. Using Presets

```python
from solvers_lib.config import SolverConfig
from solvers_lib import linear_convection_1d

config = SolverConfig.load_preset('linear_convection_1d')
result = linear_convection_1d(**config.__dict__)
```

### 4. Web API Style

```python
from solvers_lib.web_api import WebSolverAPI

# List available solvers
solvers = WebSolverAPI.get_available_solvers()

# Run solver
result = WebSolverAPI.solve('linear_convection_1d', {
    'nx': 51,
    'nt': 30
})

# Output is JSON-serializable
```

### 5. Run Flask Web App

```bash
cd src
python flask_app.py
# Open browser to http://localhost:5000
```

**Test endpoints:**
```bash
# List solvers
curl http://localhost:5000/api/solvers

# Run solver with preset
curl http://localhost:5000/api/solve/linear_convection_1d

# Run with custom config
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"solver_name": "linear_convection_1d", "config": {"nx": 51}}'
```

## All Available Solvers

### 1D Problems
- `linear_convection_1d` - Wave equation
- `diffusion_1d` - Heat equation  
- `nonlinear_convection_1d` - Burger's equation
- `burgers_1d` - Burger's with viscosity

### 2D Problems
- `linear_convection_2d` - 2D wave
- `nonlinear_convection_2d` - 2D nonlinear wave
- `diffusion_2d` - 2D heat
- `laplace_2d` - Laplace equation
- `poisson_2d` - Poisson equation
- `cavity_flow_navier_stokes` - Lid-driven cavity

## Common Patterns

### Custom Initial Condition

```python
import numpy as np
from solvers_lib import linear_convection_1d

x = np.linspace(0, 2, 41)
ic = np.sin(np.pi * x)

result = linear_convection_1d(
    nx=41,
    nt=20,
    initial_condition=ic
)
```

### Batch Processing

```python
from solvers_lib.web_api import WebSolverAPI

for solver in ['linear_convection_1d', 'diffusion_1d']:
    result = WebSolverAPI.solve(solver)
    print(f"{solver}: min={result['u'].min()}, max={result['u'].max()}")
```

### JSON Export

```python
import json
from solvers_lib.web_api import NumpyJSONEncoder
from solvers_lib import linear_convection_1d

result = linear_convection_1d()
json_str = json.dumps(result, cls=NumpyJSONEncoder)

# Save or send over HTTP
with open('result.json', 'w') as f:
    f.write(json_str)
```

### Change Parameters

```python
# Lower resolution (fast)
result_fast = linear_convection_1d(nx=21, nt=10)

# Higher resolution (slow, accurate)
result_accurate = linear_convection_1d(nx=101, nt=100)

# Different physics parameters
result_wave = linear_convection_1d(c=1.5, sigma=0.5)
result_diffusion = diffusion_1d(nu=0.5)
```

## Test Everything

```bash
cd src
python examples.py  # Runs 11 examples
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: solvers_lib` | Add `src/` to PYTHONPATH |
| Solution diverges | Reduce `dt`, increase `sigma` |
| Slow execution | Reduce `nx`, `ny`, `nt` |
| Memory error | Use coarser grid |
| JSON serialization fails | Use `NumpyJSONEncoder` |

## Output Structure

All solvers return a dictionary:

```python
{
    'x': array,              # Grid points (1D or 2D)
    'y': array,              # Grid points (2D only)
    'u': array,              # Solution field
    'v': array,              # Velocity field (some solvers)
    'p': array,              # Pressure field (NS only)
    'history': array,        # Solution history
    'dx': float,             # Grid spacing
    'dy': float,             # Grid spacing (2D)
    'dt': float,             # Time step
    't_final': float,        # Final time
    'config': dict,          # Parameters used
}
```

## Next Steps

1. **Test**: Run `examples.py` to verify setup
2. **Explore**: Review solver docstrings
3. **Integrate**: Use in your web app
4. **Visualize**: Add plotting layer
5. **Deploy**: Package for production

## Documentation

- Full docs: `src/solvers_lib/README.md`
- Integration guide: `REFACTORING_GUIDE.md`
- API examples: `src/examples.py`
- Flask app: `src/flask_app.py`

## Get Help

```python
from solvers_lib import linear_convection_1d
help(linear_convection_1d)  # Show docstring
```

---

**Ready?** Start with:
```bash
cd src
python -c "from solvers_lib import linear_convection_1d; print(linear_convection_1d())"
```
