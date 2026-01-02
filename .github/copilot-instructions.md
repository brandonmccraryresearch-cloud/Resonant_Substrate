# GitHub Copilot Instructions for Resonant Substrate

This repository implements the Intrinsic Resonance Holography (IRH) computational framework.

## Project Context

IRH is a theoretical physics framework that transitions from an informational ontology to a vibrational one, proposing that reality emerges from a four-strand intrinsic resonant substrate.

## Development Guidelines

### Code Style
- Follow PEP 8 strictly
- Use type hints for all function parameters and returns
- Maximum line length: 100 characters
- Format with `black --line-length 100`
- Lint with `ruff`

### Documentation
- Use NumPy-style docstrings
- Include equation references from IRH manuscripts
- Document all public APIs comprehensively
- Provide usage examples

### Testing
- Write tests for all new functionality
- Maintain >80% code coverage
- Use pytest for testing
- Include both unit and integration tests

### Physics Accuracy
- All physical constants should reference IRH theory
- Cite specific equations from documentation
- Validate against known experimental results
- Document theoretical assumptions

## Key Modules

- `irh.core.framework`: Main IRH computational framework
- `irh.physics`: Physics calculations and derivations
- `irh.optimization`: Parameter optimization routines
- `irh.utils`: Utility functions

## Before Committing

1. Run tests: `pytest tests/ -v`
2. Check formatting: `black --check src/ tests/`
3. Lint code: `ruff check src/ tests/`
4. Type check: `mypy src/irh/`

## References

- IRH Documentation: `docs/newfoundation/`
- Copilot Instructions: `docs/newfoundation/copilot-instructions.md`
- Computational Framework: `docs/newfoundation/IRH_Computational_Fra.md`
