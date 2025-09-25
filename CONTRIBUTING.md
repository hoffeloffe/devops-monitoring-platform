# Contributing to DevOps Automation Hub

Thank you for your interest in contributing to the DevOps Automation Hub! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose
- Git
- Basic knowledge of DevOps concepts

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/devops-automation-hub.git
   cd devops-automation-hub
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start Development Services**
   ```bash
   docker-compose -f docker-compose.simple.yml up -d
   python src/app.py
   ```

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use Black for code formatting: `black .`
- Use isort for import sorting: `isort .`
- Use flake8 for linting: `flake8 .`

### Commit Messages
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(api): add cost optimization endpoint
fix(dashboard): resolve chart rendering issue
docs(readme): update installation instructions
```

### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation updates

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

### Writing Tests
- Place tests in the `tests/` directory
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies

Example:
```python
def test_health_endpoint_returns_success():
    # Arrange
    client = app.test_client()
    
    # Act
    response = client.get('/api/health')
    
    # Assert
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
```

## 📁 Project Structure

```
devops-automation-hub/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
├── src/
│   ├── api/               # REST API endpoints
│   ├── automation/        # Core automation modules
│   ├── config/           # Configuration management
│   └── utils/            # Utility functions
├── tests/                # Test files
├── docs/                 # Additional documentation
├── docker/               # Docker configurations
├── scripts/              # Utility scripts
└── dashboard.html        # Web dashboard
```

## 🔧 Adding New Features

### API Endpoints
1. Create endpoint in appropriate module under `src/api/`
2. Add input validation using Flask-WTF or similar
3. Include proper error handling
4. Add comprehensive tests
5. Update API documentation

### Automation Modules
1. Create module in `src/automation/`
2. Follow the base automation class pattern
3. Include configuration options
4. Add logging and error handling
5. Write unit and integration tests

### Dashboard Features
1. Update `dashboard.html` with new UI components
2. Ensure responsive design
3. Add appropriate JavaScript functionality
4. Test across different browsers
5. Update documentation

## 📊 Performance Guidelines

- Use async/await for I/O operations where possible
- Implement proper caching strategies
- Monitor memory usage in long-running processes
- Use database indexing appropriately
- Profile code for bottlenecks

## 🔒 Security Considerations

- Never commit secrets or credentials
- Use environment variables for configuration
- Validate all user inputs
- Implement proper authentication/authorization
- Follow OWASP security guidelines

## 📝 Documentation

- Update README.md for significant changes
- Add docstrings to all functions and classes
- Update API documentation
- Include examples in documentation
- Keep CHANGELOG.md updated

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages

## 💡 Feature Requests

For feature requests, please provide:
- Clear description of the feature
- Use case and business value
- Proposed implementation approach
- Any relevant examples or mockups

## 🚀 Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   pytest
   flake8 .
   black --check .
   isort --check-only .
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub

6. **PR Requirements**
   - Clear title and description
   - Link to related issues
   - All tests passing
   - Code review approval
   - Up-to-date with main branch

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributor graphs

## 📞 Getting Help

- Create an issue for bugs or feature requests
- Join our discussions for questions
- Check existing documentation first
- Be respectful and constructive

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to DevOps Automation Hub! 🚀
