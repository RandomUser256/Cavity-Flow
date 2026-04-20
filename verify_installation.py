#!/usr/bin/env python
"""
Verification script for the refactored solvers library.
Run this to ensure everything is installed and working correctly.
"""

import sys
import os
import json

def check_imports():
    """Check if all required modules can be imported."""
    print("✓ Checking imports...")
    
    try:
        import numpy
        print("  ✓ numpy")
    except ImportError as e:
        print(f"  ✗ numpy: {e}")
        return False
    
    try:
        from solvers_lib import (
            linear_convection_1d,
            linear_convection_2d,
            cavity_flow_navier_stokes
        )
        print("  ✓ solvers_lib")
    except ImportError as e:
        print(f"  ✗ solvers_lib: {e}")
        print("    Make sure src/ is in Python path")
        return False
    
    try:
        from solvers_lib.config import SolverConfig
        print("  ✓ config module")
    except ImportError as e:
        print(f"  ✗ config: {e}")
        return False
    
    try:
        from solvers_lib.web_api import WebSolverAPI
        print("  ✓ web_api module")
    except ImportError as e:
        print(f"  ✗ web_api: {e}")
        return False
    
    return True


def check_solvers():
    """Check if all solvers work."""
    print("\n✓ Testing solvers...")
    
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
    
    solvers = {
        'linear_convection_1d': {'nx': 21, 'nt': 5},
        'diffusion_1d': {'nx': 21, 'nt': 5},
        'nonlinear_convection_1d': {'nx': 21, 'nt': 5, 'dt': 0.025},
        'burgers_1d': {'nx': 51, 'nt': 20},
        'linear_convection_2d': {'nx': 21, 'ny': 21, 'nt': 5},
        'nonlinear_convection_2d': {'nx': 21, 'ny': 21, 'nt': 5},
        'diffusion_2d': {'nx': 21, 'ny': 21, 'nt': 5},
        'laplace_2d': {'nx': 21, 'ny': 21},
        'poisson_2d': {'nx': 21, 'ny': 21, 'nt': 20},
        'cavity_flow_navier_stokes': {'nx': 21, 'ny': 21, 'nt': 10},
    }
    
    solver_funcs = {
        'linear_convection_1d': linear_convection_1d,
        'diffusion_1d': diffusion_1d,
        'nonlinear_convection_1d': nonlinear_convection_1d,
        'burgers_1d': burgers_1d,
        'linear_convection_2d': linear_convection_2d,
        'nonlinear_convection_2d': nonlinear_convection_2d,
        'diffusion_2d': diffusion_2d,
        'laplace_2d': laplace_2d,
        'poisson_2d': poisson_2d,
        'cavity_flow_navier_stokes': cavity_flow_navier_stokes,
    }
    
    for name, func in solver_funcs.items():
        try:
            result = func(**solvers[name])
            assert 'u' in result or 'p' in result, f"Missing solution in {name}"
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            return False
    
    return True


def check_config():
    """Check configuration system."""
    print("\n✓ Testing configuration system...")
    
    from solvers_lib.config import SolverConfig
    
    try:
        # Test preset loading
        config = SolverConfig.load_preset('linear_convection_1d')
        print("  ✓ Load preset")
        
        # Test to_dict
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        print("  ✓ to_dict()")
        
        # Test to_json
        config_json = config.to_json()
        assert isinstance(config_json, str)
        print("  ✓ to_json()")
        
        # Test from_json
        config2 = SolverConfig.from_json(config_json)
        assert config.nx == config2.nx
        print("  ✓ from_json()")
        
        # Test all presets available
        presets = SolverConfig.get_all_presets()
        assert len(presets) >= 10
        print(f"  ✓ All presets ({len(presets)} available)")
        
        return True
    except Exception as e:
        print(f"  ✗ Configuration: {e}")
        return False


def check_web_api():
    """Check web API."""
    print("\n✓ Testing web API...")
    
    from solvers_lib.web_api import WebSolverAPI, NumpyJSONEncoder
    import json
    
    try:
        # Test get_available_solvers
        solvers = WebSolverAPI.get_available_solvers()
        assert '1d_solvers' in solvers
        assert '2d_solvers' in solvers
        print("  ✓ get_available_solvers()")
        
        # Test solve
        result = WebSolverAPI.solve('linear_convection_1d', {
            'nx': 21,
            'nt': 5
        })
        assert 'u' in result
        assert 'config' in result
        print("  ✓ solve()")
        
        # Test JSON serialization
        json_str = json.dumps(result, cls=NumpyJSONEncoder)
        assert isinstance(json_str, str)
        json_obj = json.loads(json_str)
        assert 'u' in json_obj
        print("  ✓ JSON serialization")
        
        return True
    except Exception as e:
        print(f"  ✗ Web API: {e}")
        return False


def check_flask():
    """Check if Flask dependencies are available."""
    print("\n✓ Checking Flask dependencies...")
    
    try:
        import flask
        print("  ✓ Flask installed")
    except ImportError:
        print("  ⚠ Flask not installed (optional)")
        print("    pip install Flask Flask-CORS")
        return True
    
    try:
        from flask_cors import CORS
        print("  ✓ Flask-CORS installed")
    except ImportError:
        print("  ⚠ Flask-CORS not installed (optional)")
        return True
    
    return True


def main():
    """Run all checks."""
    print("\n" + "=" * 60)
    print(" Refactored Solvers Library - Verification")
    print("=" * 60 + "\n")
    
    # Add src to path if needed
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if os.path.exists(src_path) and src_path not in sys.path:
        sys.path.insert(0, src_path)
        print(f"Added {src_path} to Python path\n")
    
    checks = [
        ("Imports", check_imports),
        ("Solvers", check_solvers),
        ("Configuration", check_config),
        ("Web API", check_web_api),
        ("Flask (optional)", check_flask),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name}: Unexpected error: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print(" Summary")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total or (passed == total - 1 and not results[-1][1]):  # Allow Flask to fail
        print("\n✓ Library is ready for use!")
        print("\nNext steps:")
        print("  1. Run examples: python src/examples.py")
        print("  2. Start Flask app: python src/flask_app.py")
        print("  3. Read docs: QUICK_START.md, REFACTORING_GUIDE.md")
        return 0
    else:
        print("\n✗ Some checks failed. Please install dependencies:")
        print("  pip install -r src/solvers_lib/requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
