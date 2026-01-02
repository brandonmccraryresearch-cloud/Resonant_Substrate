# Contributing to Resonant Substrate

Thank you for your interest in contributing to the Resonant Substrate project! This document provides guidelines for contributing to the IRH computational framework.

## Code of Conduct

This project adheres to a code of conduct that promotes an open, welcoming, and inclusive community. All contributors are expected to uphold these values.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Resonant_Substrate.git`
3. Create a virtual environment: `python -m venv irh_env && source irh_env/bin/activate`
4. Install dependencies: `pip install -e .[dev]`
5. Create a feature branch: `git checkout -b feature/your-feature-name`

## Development Guidelines

### Code Style

- Follow PEP 8 conventions strictly
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use descriptive variable and function names
- Add docstrings to all public functions and classes

### Documentation

- Use NumPy-style docstrings
- Include equation references from IRH manuscripts where applicable
- Provide usage examples in docstrings
- Update README.md if adding new features
- Document theoretical assumptions and derivations

### Testing

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use pytest for testing
- Include both unit tests and integration tests
- Test edge cases and error conditions

### Commit Messages

Use clear, descriptive commit messages following this format:

```
<type>: <short summary>

<detailed explanation if needed>

Fixes #<issue-number>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`

## Pull Request Process

1. Update documentation for any changed functionality
2. Add tests for new features
3. Ensure all tests pass: `pytest tests/ -v`
4. Format code: `black src/ tests/ examples/ --line-length 100`
5. Lint code: `ruff check src/ tests/ examples/`
6. Update CHANGELOG.md if applicable
7. Create a pull request with a clear description

### PR Checklist

- [ ] Tests pass locally
- [ ] Code is formatted with black
- [ ] Code passes ruff linting
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Docstrings complete
- [ ] CHANGELOG.md updated (for significant changes)

## Reporting Bugs

Please use GitHub Issues to report bugs. Include:

- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version and dependencies
- Minimal code example if applicable

## Suggesting Features

Feature requests are welcome! Please use GitHub Issues with the "enhancement" label. Include:

- Clear description of the proposed feature
- Use cases and motivation
- Potential implementation approach
- Relationship to IRH theory

## Code Review Process

All submissions require review before merging:

1. Automated CI checks must pass
2. At least one maintainer approval required
3. Code must meet style guidelines
4. Tests must achieve adequate coverage
5. Documentation must be complete

## Physics Accuracy

This project implements theoretical physics. Special attention is required:

- **Cite equations**: Reference specific equations from IRH manuscripts
- **Validate results**: Compare with known experimental data where possible
- **Document assumptions**: Clearly state theoretical assumptions
- **Unit testing**: Verify physical consistency (unitarity, conservation laws, etc.)
- **Numerical stability**: Ensure algorithms are numerically stable

## Questions?

- Open a GitHub Discussion for general questions
- Use GitHub Issues for bugs and feature requests
- Check existing documentation in `docs/` directory

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to advancing fundamental physics research!
