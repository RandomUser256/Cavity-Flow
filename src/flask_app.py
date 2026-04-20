"""
Example Flask web app for the solvers library.
This demonstrates how to integrate the refactored solvers into a web application.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from solvers_lib.web_api import WebSolverAPI, NumpyJSONEncoder
from solvers_lib.config import SolverConfig

app = Flask(__name__)
CORS(app)

# Custom JSON encoder for numpy arrays
app.json_encoder = NumpyJSONEncoder


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


@app.route('/api/solvers', methods=['GET'])
def get_solvers():
    """Get list of available solvers."""
    solvers = WebSolverAPI.get_available_solvers()
    return jsonify(solvers)


@app.route('/api/presets', methods=['GET'])
def get_presets():
    """Get list of available presets."""
    presets = list(SolverConfig.get_all_presets().keys())
    return jsonify({'presets': presets})


@app.route('/api/preset/<preset_name>', methods=['GET'])
def get_preset(preset_name):
    """Get a specific preset."""
    try:
        config = SolverConfig.load_preset(preset_name)
        return jsonify(config.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@app.route('/api/solve', methods=['POST'])
def solve():
    """
    Solve endpoint.
    
    Request JSON format:
    {
        "solver_name": "linear_convection_1d",
        "config": {
            "nx": 41,
            "nt": 20,
            ...
        },
        "include_history": false
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'solver_name' not in data:
            return jsonify({'error': 'Missing solver_name'}), 400
        
        solver_name = data['solver_name']
        config = data.get('config')
        include_history = data.get('include_history', False)
        
        # Run solver
        result = WebSolverAPI.solve(solver_name, config, include_history)
        
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Solver error: {str(e)}'}), 500


@app.route('/api/solve/<solver_name>', methods=['GET', 'POST'])
def solve_by_name(solver_name):
    """
    Convenience endpoint for solving by solver name.
    GET: uses default preset
    POST: uses provided config
    """
    try:
        include_history = request.args.get('include_history', 'false').lower() == 'true'
        
        if request.method == 'POST':
            config = request.get_json()
        else:
            config = None
        
        result = WebSolverAPI.solve(solver_name, config, include_history)
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Solver error: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
