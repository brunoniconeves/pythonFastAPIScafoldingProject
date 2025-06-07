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
- Docker support with multi-stage builds
- Database migrations with Alembic

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
├── alembic/             # Database migrations
│   ├── versions/        # Migration versions
│   └── env.py          # Alembic configuration
├── tests/               # Test suite
│   ├── test_config.py   # Configuration tests
│   ├── test_health.py   # Health check endpoint tests
│   ├── test_repositories.py  # Repository layer tests
│   ├── test_services.py     # Service layer tests
│   └── test_users.py        # User endpoints tests
├── scripts/             # Utility scripts
│   └── init.sh         # Container initialization script
├── .coveragerc          # Coverage configuration
├── codecov.yml          # Codecov configuration
├── pytest.ini          # Pytest configuration
├── requirements.txt    # Project dependencies
├── alembic.ini        # Alembic configuration
├── Dockerfile         # Docker build instructions
├── docker-compose.yml # Docker Compose configuration
└── README.md          # Project documentation
```

## Setup

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/brunoniconeves/pythonFastAPIScafoldingProject.git
cd pythonFastAPIScafoldingProject
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the database migrations:
```bash
python -m alembic upgrade head
```

4. Run the tests:
```bash
pytest --cov=app --cov-report=term-missing
```

5. Start the server:
```bash
uvicorn app.main:app --reload
```

### Docker Setup

The application can be run using Docker, which provides an isolated environment with all necessary dependencies.

#### Prerequisites
- Docker installed on your system
- Docker Compose installed on your system

#### Running with Docker Compose (Recommended)

1. Build and start the container:
```bash
docker compose up --build
```

This command will:
- Build the Docker image using multi-stage builds for optimization
- Create and initialize the SQLite database
- Run database migrations automatically
- Start the FastAPI application
- Enable automatic restarts on failure
- Mount a volume for persistent database storage

The API will be available at http://localhost:8000

To stop the container:
```bash
docker compose down
```

#### Running with Docker Directly

Alternatively, you can run the container using Docker commands:

1. Build the image:
```bash
docker build -t fastapi-microservice .
```

2. Run the container:
```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data fastapi-microservice
```

#### Docker Configuration Features
- **Multi-stage builds**: Optimized image size
- **Non-root user**: Enhanced security
- **Volume mounting**: Persistent database storage in `./data`
- **Health checks**: Automatic container health monitoring
- **Automatic restarts**: Container recovers from failures
- **Environment variables**: Configurable through Docker Compose

#### Accessing Logs
To view container logs:
```bash
# Follow logs in real-time
docker compose logs -f

# View specific number of lines
docker compose logs --tail=100
```

#### Database Management
The SQLite database is persisted in the `./data` directory. To reset the database:
1. Stop the containers: `docker compose down`
2. Delete the database file: `rm data/app.db`
3. Restart the containers: `docker compose up --build`

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