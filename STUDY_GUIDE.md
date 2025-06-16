# Python Interview Study Guide

## 1. Python Fundamentals
- Data Types: int, float, str, list, tuple, dict, set
- List comprehensions and generator expressions
- Functions: args, kwargs, decorators, lambda functions
- Object-Oriented Programming: classes, inheritance, polymorphism
- Context managers (with statement)
- Exception handling (try/except/finally)

## 2. Python-Specific Features
- GIL (Global Interpreter Lock)
- Memory management and garbage collection
- Mutable vs Immutable types
- Iterators and Generators
- Magic methods (__init__, __str__, etc.)
- Module import system
- Virtual environments

## 3. Common Standard Library Modules
- collections (defaultdict, Counter, namedtuple)
- datetime
- json
- os and sys
- re (regular expressions)
- threading and multiprocessing

## 4. Modern Python Development (as shown in this repo)
- FastAPI for REST APIs
- SQLAlchemy for ORM
- Pydantic for data validation
- pytest for testing
- Dependency injection patterns
- Async/await programming

## 5. Design Patterns & Best Practices
- Repository pattern (see app/repositories)
- Service layer pattern (see app/services)
- Dependency injection (see app/dependencies)
- SOLID principles
- Clean Architecture

## 6. Common Interview Tasks
- String manipulation
- List/array operations
- Dictionary operations
- Basic algorithms (sorting, searching)
- Problem-solving approaches

## 7. Testing Knowledge (from our repo)
- Unit testing with pytest
- Fixtures
- Mocking
- Test organization
- Test coverage

## 8. Database Knowledge
- SQL basics
- ORM concepts
- Migrations
- CRUD operations
- Relationships

## Practice Tips:
1. Review each concept in this repository
2. Write code without IDE assistance
3. Explain the code structure out loud
4. Practice implementing basic algorithms
5. Review common interview questions

## Key Files in This Repo for Reference:
- `app/models/` - Database models
- `app/schemas/` - Pydantic schemas
- `app/services/` - Business logic
- `app/repositories/` - Data access
- `tests/` - Testing examples 