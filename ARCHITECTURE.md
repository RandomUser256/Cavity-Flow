# Architecture & Design Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Applications                         │
│  (Flask, FastAPI, Streamlit, Static Frontend, Mobile)     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Web API Layer                            │
│  (flask_app.py, FastAPI adapters, REST endpoints)         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              WebSolverAPI (web_api.py)                     │
│  • JSON serialization (NumpyJSONEncoder)                  │
│  • Solver routing & parameter mapping                     │
│  • Configuration validation                               │
│  • Batch processing                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│          SolverConfig (config.py)                          │
│  • Parameter management                                   │
│  • 10+ presets (linear_conv, diffusion, etc.)            │
│  • JSON export/import                                     │
│  • Validation & defaults                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
┌────────▼─────────┐        ┌──────▼────────────┐
│  1D Solvers      │        │   2D Solvers     │
│                  │        │                  │
│ • Linear Conv    │        │ • Linear Conv    │
│ • Diffusion      │        │ • Nonlin Conv    │
│ • Nonlin Conv    │        │ • Diffusion      │
│ • Burgers Eq     │        │ • Laplace        │
│ (solvers_1d.py)  │        │ • Poisson        │
│                  │        │ • Cavity Flow NS │
└────────┬─────────┘        │ (solvers_2d.py)  │
         │                  └──────┬────────────┘
         │                        │
         └────────────┬───────────┘
                      │
         ┌────────────▼────────────┐
         │  Utilities (utils.py)   │
         │  • Grid generation      │
         │  • Initial conditions   │
         │  • Boundary conditions  │
         │  • CFL calculations     │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │  NumPy / Scientific    │
         │  Computing Stack       │
         └────────────────────────┘
```

## Data Flow

### Typical Request Flow

```
User Request (JSON)
        │
        ▼
┌──────────────────────┐
│ Parse Request        │
│ {solver, config}     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Create SolverConfig  │
│ Validate parameters  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Route to Solver      │
│ Map parameters       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────┐
│ Execute Solver                   │
│ • Grid generation                │
│ • Time stepping                  │
│ • BC application                 │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ Return Result Dict               │
│ numpy arrays + metadata           │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ Serialize to JSON                │
│ (NumpyJSONEncoder)               │
└──────────┬───────────────────────┘
           │
           ▼
Response (JSON)
```

## Module Responsibilities

### `utils.py` - Foundational Tools
- Grid generation (1D/2D uniform grids)
- Initial conditions (hat functions, custom)
- Boundary condition application
- CFL/stability calculations
- **Dependency**: None (pure numpy)

### `solvers_1d.py` - 1D Physics
- Implements 4 PDE solvers
- Uses utilities for setup
- Returns data dictionaries
- **Dependency**: utils, numpy

### `solvers_2d.py` - 2D Physics  
- Implements 6 PDE solvers
- Includes cavity flow (Navier-Stokes)
- Iterative elliptic solvers
- **Dependency**: utils, numpy

### `config.py` - Parameter Management
- `SolverConfig` dataclass
- 10+ presets for each solver
- JSON serialization
- **Dependency**: None (builtin)

### `web_api.py` - Integration Layer
- `WebSolverAPI` static class
- `NumpyJSONEncoder` custom encoder
- Routes requests to solvers
- Parameter mapping & validation
- **Dependency**: all modules, json

### `flask_app.py` - Web Server
- HTTP endpoints
- CORS support
- Error handling
- **Dependency**: Flask, web_api

## Key Design Decisions

### 1. **No Plotting**
- Separates computation from visualization
- Enables headless/backend use
- Reduces dependencies
- Users can add plotting layer

### 2. **Dictionary Output**
- Standardized across all solvers
- Contains metadata with results
- Easy JSON serialization
- Extensible for new solvers

### 3. **Configuration Objects**
- `SolverConfig` dataclass
- Type-safe parameter passing
- Validation in one place
- JSON import/export

### 4. **Static Web API Class**
- No state management needed
- Pure functions
- Easy to scale/parallelize
- REST-friendly

### 5. **Modular Solvers**
- Each solver is independent
- Easy to add new solvers
- Can be used in isolation
- No interdependencies

## Extension Points

### Add New Solver

```python
# In solvers_1d.py or solvers_2d.py
def my_new_solver(nx, nt, **params) -> Dict:
    """New solver docstring."""
    # Implementation
    return {
        'x': x,
        'u': u,
        'history': history,
        # ... metadata
    }

# In __init__.py
from .solvers_1d import my_new_solver
__all__.append('my_new_solver')

# In config.py
@staticmethod
def preset_my_new_solver():
    return SolverConfig(...)

# Automatically available in web API!
```

### Add Visualization

```python
# New module: plotting.py
from matplotlib import pyplot as plt
from solvers_lib import linear_convection_1d

def plot_1d_result(result):
    plt.plot(result['x'], result['u'])
    
    # Optional: animate history
    for step in result['history']:
        plt.plot(result['x'], step)
    plt.show()

# Use:
result = linear_convection_1d()
plot_1d_result(result)
```

### Add Database Persistence

```python
import json
from solvers_lib.web_api import NumpyJSONEncoder

def save_result(db, solver_name, result):
    db.insert({
        'solver': solver_name,
        'config': result['config'],
        'solution': json.dumps(result['u'], cls=NumpyJSONEncoder),
        'timestamp': datetime.now()
    })
```

### Add Caching

```python
from functools import lru_cache
from solvers_lib.web_api import WebSolverAPI

@lru_cache(maxsize=32)
def solve_cached(solver_name, config_json):
    config = json.loads(config_json)
    return WebSolverAPI.solve(solver_name, config)
```

## Performance Characteristics

### Computational Complexity
```
1D Linear Convection:   O(nx * nt)
1D Diffusion:           O(nx * nt)
2D Linear Convection:   O(nx * ny * nt)
2D Cavity Flow:         O(nx * ny * nt * nit)
Laplace (Iterative):    O(nx * ny * iterations)
```

### Memory Usage
```
1D Solution:            O(nx)
1D History:             O(nx * nt)
2D Solution:            O(nx * ny)
2D History:             O(nx * ny * nt)
```

### Timing Estimates (1 GHz CPU)
```
nx=21, nt=10:           ~1-5 ms
nx=41, nt=20:           ~10-50 ms
nx=101, nt=100:         ~100-500 ms
2D: nx=41, ny=41, nt=50: ~1-2 sec
Cavity: nx=41, nt=500:   ~5-10 sec
```

## Testing Strategy

### Unit Tests (should be added)
```python
def test_linear_convection_1d():
    result = linear_convection_1d(nx=21, nt=10)
    assert result['u'].shape == (21,)
    assert 'history' in result
    assert result['t_final'] > 0

def test_config_serialization():
    cfg = SolverConfig(nx=41, nt=20)
    json_str = cfg.to_json()
    cfg2 = SolverConfig.from_json(json_str)
    assert cfg.nx == cfg2.nx
```

### Integration Tests (should be added)
```python
def test_web_api_solve():
    result = WebSolverAPI.solve('linear_convection_1d')
    assert result['solver_name'] == 'linear_convection_1d'
    assert isinstance(result['u'], list)  # JSON serialized
```

## Deployment Strategy

### Development
```
├── Source: src/solvers_lib/
├── Testing: pytest
└── Docs: Markdown in src/
```

### Production (Single Server)
```
├── Docker container
├── Flask app on port 5000
├── Max time limit per request
└── Health checks & monitoring
```

### Production (Scaled)
```
├── Multiple worker containers
├── Load balancer (nginx)
├── Request queuing (celery)
├── Result caching (redis)
└── Database (PostgreSQL)
```

---

**This architecture is:**
- ✅ Modular & extensible
- ✅ Web-ready & REST-friendly
- ✅ Testable & maintainable
- ✅ Scalable & performant
- ✅ Well-documented & clean
