# Contributing to Enhanced MCP Your Turn Server

Thank you for your interest in contributing to the Enhanced MCP Your Turn Server! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Check existing issues** first to avoid duplicates
2. **Use the issue templates** when available
3. **Provide detailed information**:
   - Operating system and version
   - Python version
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Error messages and logs

### Suggesting Features

1. **Open a feature request** issue
2. **Describe the use case** and motivation
3. **Provide examples** of how the feature would be used
4. **Consider backward compatibility** implications

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch** from `main`
3. **Make your changes** following our coding standards
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Submit a pull request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- Optional: Docker for containerized development

### Local Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/your-turn-mcp.git
cd your-turn-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy
```

### Running Tests

```bash
# Run all tests
python3 -m pytest

# Run with coverage
python3 -m pytest --cov=. --cov-report=html

# Run specific test file
python3 -m pytest tests/test_sound_manager.py

# Test individual components
python3 sound_manager.py
python3 interactive_session.py
```

## 📝 Coding Standards

### Python Style Guide

- Follow **PEP 8** Python style guidelines
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions and classes
- Keep line length under **88 characters** (Black formatter default)

### Code Formatting

We use **Black** for code formatting:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .
```

### Linting

We use **flake8** for linting:

```bash
# Run linter
flake8 .

# With specific configuration
flake8 --max-line-length=88 --extend-ignore=E203,W503 .
```

### Type Checking

We use **mypy** for type checking:

```bash
# Run type checker
mypy .

# Check specific file
mypy mcp_your_turn_server.py
```

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use **pytest** framework
- Follow the **Arrange-Act-Assert** pattern
- Use descriptive test names

Example test structure:

```python
import pytest
from your_module import YourClass

class TestYourClass:
    def test_method_with_valid_input_returns_expected_result(self):
        # Arrange
        instance = YourClass()
        input_data = "test_input"
        
        # Act
        result = instance.your_method(input_data)
        
        # Assert
        assert result == "expected_output"
    
    @pytest.mark.asyncio
    async def test_async_method(self):
        # Test async methods
        instance = YourClass()
        result = await instance.async_method()
        assert result is not None
```

### Test Categories

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

### Mocking

Use **unittest.mock** for external dependencies:

```python
from unittest.mock import patch, MagicMock

@patch('telegram_notifier.Bot')
def test_telegram_notification(mock_bot):
    mock_bot.return_value.send_message = MagicMock()
    # Test implementation
```

## 📚 Documentation

### Code Documentation

- Write clear **docstrings** for all public APIs
- Use **Google-style docstrings**:

```python
def your_function(param1: str, param2: int) -> bool:
    """Brief description of the function.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        Description of return value.
        
    Raises:
        ValueError: When param1 is invalid.
    """
```

### README Updates

- Update README.md for user-facing changes
- Update DEVELOPER.md for technical changes
- Include examples for new features

## 🔄 Pull Request Process

### Before Submitting

1. **Ensure all tests pass**
2. **Run code formatting and linting**
3. **Update documentation**
4. **Add changelog entry** if applicable

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Testing** in different environments
4. **Approval** and merge

## 🏗️ Architecture Guidelines

### Modular Design

- Keep components **loosely coupled**
- Use **dependency injection** where appropriate
- Follow **single responsibility principle**

### Error Handling

- Use **specific exception types**
- Provide **meaningful error messages**
- Implement **graceful degradation**

### Async Programming

- Use **asyncio** for I/O operations
- Implement proper **timeout handling**
- Avoid **blocking operations** in async code

## 🔒 Security Guidelines

### Input Validation

- **Validate all inputs** from external sources
- **Sanitize user data** before processing
- Use **parameterized queries** for database operations

### Secrets Management

- **Never commit secrets** to version control
- Use **environment variables** for configuration
- Document **required environment variables**

### Dependencies

- Keep dependencies **up to date**
- Review **security advisories**
- Use **pinned versions** in production

## 📋 Issue Labels

We use the following labels to categorize issues:

- **bug**: Something isn't working
- **enhancement**: New feature or request
- **documentation**: Improvements or additions to documentation
- **good first issue**: Good for newcomers
- **help wanted**: Extra attention is needed
- **question**: Further information is requested

## 🎯 Roadmap

### Current Priorities

1. **Stability improvements**
2. **Additional notification channels**
3. **Enhanced interactive features**
4. **Performance optimizations**

### Future Goals

- Web interface for configuration
- Plugin system for extensions
- Advanced session management
- Multi-language support

## 💬 Communication

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Developer Documentation**: For technical details

### Code of Conduct

- Be **respectful** and **inclusive**
- **Constructive feedback** only
- **Help others** learn and grow
- **Follow community guidelines**

## 🏆 Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions
- **GitHub contributors** section

Thank you for contributing to the Enhanced MCP Your Turn Server! 🚀
