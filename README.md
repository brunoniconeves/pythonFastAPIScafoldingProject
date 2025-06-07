# FastAPI Microservice

[![Tests](https://github.com/brunoniconeves/pythonFastAPIScafoldingProject/actions/workflows/test.yml/badge.svg)](https://github.com/brunoniconeves/pythonFastAPIScafoldingProject/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/brunoniconeves/pythonFastAPIScafoldingProject/branch/main/graph/badge.svg)](https://codecov.io/gh/brunoniconeves/pythonFastAPIScafoldingProject)

A well-structured FastAPI microservice with proper configuration management, database handling, and comprehensive test coverage.

## Features

- FastAPI-based REST API
- SQLAlchemy with SQLite database
- Pydantic for data validation
- Comprehensive test suite with 100% coverage
- GitHub Actions CI pipeline
- Codecov integration

## Project Structure

```
.
├── app/
│   ├── core/           # Core functionality (config, etc.)
│   ├── models/         # SQLAlchemy models
│   ├── repositories/   # Data access layer
│   ├── routers/        # API endpoints
│   ├── schemas/        # Pydantic models
│   └── services/       # Business logic
├── tests/              # Test suite
└── requirements.txt    # Project dependencies
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
pytest
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
- `GET /api/v1/system/health` - Health check
- `GET /api/v1/system/config` - System configuration

### Users
- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create new user

## Testing

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

View coverage report in `coverage_html/index.html`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 