# FastAPI Microservice

[![Tests](https://github.com/brunoniconeves/pythonFastAPIScafoldingProject/actions/workflows/test.yml/badge.svg)](https://github.com/brunoniconeves/pythonFastAPIScafoldingProject/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/brunoniconeves/pythonFastAPIScafoldingProject/branch/main/graph/badge.svg)](https://codecov.io/gh/brunoniconeves/pythonFastAPIScafoldingProject)

A well-structured FastAPI microservice with proper configuration management, database handling, and comprehensive test coverage.

## Features

- FastAPI-based REST API
- SQLAlchemy with SQLite database
- Pydantic for data validation and settings management
- Repository pattern for data access
- Service layer for business logic
- Comprehensive test suite with 100% coverage
- GitHub Actions CI pipeline
- Codecov integration

## Project Structure

```
.
├── .github/
│   └── workflows/          # GitHub Actions workflows
│       └── test.yml       # CI pipeline configuration
├── app/
│   ├── core/              # Core functionality
│   │   └── config.py      # Application configuration
│   ├── models/            # SQLAlchemy models
│   │   └── user.py       # User model definition
│   ├── repositories/      # Data access layer
│   │   ├── base.py       # Base repository with common operations
│   │   └── user_repository.py
│   ├── routers/          # API endpoints
│   │   ├── system.py     # System endpoints (health, config)
│   │   └── users.py      # User endpoints
│   ├── schemas/          # Pydantic models
│   │   ├── system.py     # System-related schemas
│   │   └── user.py       # User-related schemas
│   ├── services/         # Business logic layer
│   │   └── user_service.py
│   ├── db.py            # Database configuration
│   └── main.py          # Application entry point
├── tests/               # Test suite
│   ├── test_config.py   # Configuration tests
│   ├── test_health.py   # Health check endpoint tests
│   ├── test_repositories.py  # Repository layer tests
│   ├── test_services.py     # Service layer tests
│   └── test_users.py        # User endpoints tests
├── .coveragerc          # Coverage configuration
├── codecov.yml          # Codecov configuration
├── pytest.ini          # Pytest configuration
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/brunoniconeves/pythonFastAPIScafoldingProject.git
cd pythonFastAPIScafoldingProject
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the tests:
```bash
pytest --cov=app --cov-report=term-missing
```

4. Start the server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- OpenAPI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Available Endpoints

### System
- `GET /api/v1/system/health` - Health check endpoint
  - Returns service status and uptime
- `GET /api/v1/system/config` - Configuration endpoint
  - Returns non-sensitive configuration settings

### Users
- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create new user
  - Validates email format
  - Prevents duplicate emails
  - Returns created user with ID

## Testing

The project includes a comprehensive test suite:

- Unit tests for all components
- Integration tests for API endpoints
- 100% code coverage requirement
- Automated testing on multiple Python versions (3.9, 3.10, 3.11)

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

View coverage report in `coverage_html/index.html`

## CI/CD

The project uses GitHub Actions for continuous integration:

- Automated testing on push and pull requests
- Multiple Python version testing
- Code coverage reporting to Codecov
- Status badges in README

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 