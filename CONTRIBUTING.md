# Contributing to Lucifer

Thank you for your interest in contributing to Lucifer! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment
- Use this tool ethically and legally

## How to Contribute

### Reporting Bugs

1. Check if the bug is already reported in [Issues](https://github.com/yashab-cyber/lucifer/issues)
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing feature requests
2. Create an issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes following our coding standards:
   - Use Black for formatting
   - Follow PEP 8 style guide
   - Add type hints
   - Write docstrings
   - Add unit tests

4. Test your changes:
   ```bash
   pytest
   black src/lucifer
   ruff check src/lucifer
   mypy src/lucifer
   ```

5. Commit with clear messages:
   ```bash
   git commit -m "feat: add new workflow for API testing"
   ```

6. Push and create a Pull Request

### Commit Message Format

Use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Build or tooling changes

## Development Setup

```bash
# Clone repository
git clone https://github.com/yashab-cyber/lucifer.git
cd lucifer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Testing Guidelines

- Write tests for new features
- Maintain test coverage above 80%
- Test both success and error cases
- Use pytest fixtures for setup
- Mock external dependencies

## Documentation

- Update README.md for significant changes
- Add docstrings to all functions and classes
- Include usage examples
- Update API documentation

## Areas for Contribution

### High Priority

- [ ] Additional workflow templates
- [ ] Better error handling
- [ ] Performance optimizations
- [ ] Integration with more tools
- [ ] Web UI development

### Medium Priority

- [ ] Additional AI provider support
- [ ] Custom plugin system
- [ ] Enhanced reporting formats
- [ ] Multi-target support
- [ ] Database integration

### Low Priority

- [ ] Mobile companion app
- [ ] Cloud deployment guides
- [ ] Video tutorials
- [ ] Translations

## Questions?

Feel free to:
- Open a discussion on GitHub
- Ask in the Issues section
- Contact the maintainers

Thank you for contributing to Lucifer! 🔥
