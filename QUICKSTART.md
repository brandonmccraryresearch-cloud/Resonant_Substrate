# Resonant Substrate: Quick Start Guide

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Install from source

```bash
# Clone the repository
git clone https://github.com/brandonmccraryresearch-cloud/Resonant_Substrate.git
cd Resonant_Substrate

# Create and activate virtual environment
python -m venv irh_env
source irh_env/bin/activate  # Linux/Mac
# or
irh_env\Scripts\activate  # Windows

# Install dependencies
pip install -e .

# For development (includes testing tools)
pip install -e .[dev]
```

## Quick Test

Verify installation:

```bash
python -c "from irh import IRH_Framework; print('✓ Installation successful')"
```

## Basic Usage

### 1. Initialize Framework

```python
from irh import IRH_Framework

# Create framework instance
framework = IRH_Framework(grid_resolution=50)
```

### 2. Calculate CKM Matrix

```python
# Derive CKM matrix from strand geometry
ckm_matrix = framework.calculate_ckm_matrix()
print(ckm_matrix)
```

### 3. Compute Neutrino Oscillations

```python
# Calculate oscillation probabilities
L = 295e3  # Baseline distance (295 km)
E = 3.0    # Energy (GeV)
probs = framework.neutrino_oscillations(L, E)
print(probs)
```

### 4. Optimize Parameters

```python
# Optimize against experimental constraints
constraints = {
    'alpha_EM': (1/137.036, 1e-8),
    'alpha_s': (0.118, 0.001),
    'Omega_DM_Omega_b': (5.33, 0.1)
}
optimized = framework.parameter_optimization(constraints)
print(optimized)
```

## Running Examples

```bash
# Run basic usage example
python examples/basic_usage.py

# Run tests
pytest tests/ -v
```

## Jupyter Notebooks

Launch Jupyter and open the introduction notebook:

```bash
jupyter notebook notebooks/01_introduction.ipynb
```

## Documentation

- **Full Documentation**: See `docs/newfoundation/` directory
- **API Reference**: Docstrings in source code
- **Contributing**: See `CONTRIBUTING.md`
- **Changelog**: See `CHANGELOG.md`

## Getting Help

- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and discuss ideas
- **Documentation**: Check `docs/` for detailed information

## Next Steps

1. Explore the example scripts in `examples/`
2. Read through the Jupyter notebooks in `notebooks/`
3. Review the IRH theory documentation in `docs/newfoundation/`
4. Check out the contributing guidelines in `CONTRIBUTING.md`

## System Requirements

### Minimum
- CPU: Quad-core processor
- RAM: 16GB
- Python: 3.8+

### Recommended
- CPU: 8+ cores
- RAM: 32GB+
- Python: 3.11+
- GPU: CUDA-capable (optional)

## Common Issues

### Import Error

If you get `ModuleNotFoundError: No module named 'irh'`:
- Ensure you've installed the package: `pip install -e .`
- Check you're in the virtual environment: `which python`

### Test Failures

If tests fail:
- Ensure all dependencies are installed: `pip install -e .[dev]`
- Update pip: `pip install --upgrade pip`
- Check Python version: `python --version` (should be 3.8+)

## Project Structure

```
Resonant_Substrate/
├── src/irh/              # Main package
│   ├── core/            # Core framework
│   ├── physics/         # Physics modules
│   ├── optimization/    # Optimization routines
│   └── utils/           # Utilities
├── tests/               # Test suite
├── examples/            # Example scripts
├── notebooks/           # Jupyter notebooks
├── docs/                # Documentation
│   └── newfoundation/   # IRH theory docs
├── requirements.txt     # Dependencies
├── pyproject.toml      # Package config
└── README.md           # Main readme
```

## Development

To contribute to the project:

1. Read `CONTRIBUTING.md`
2. Set up development environment: `pip install -e .[dev]`
3. Make changes
4. Run tests: `pytest tests/ -v`
5. Format code: `black src/ tests/ --line-length 100`
6. Submit pull request

Happy coding with IRH! 🎉
