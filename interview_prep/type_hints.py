"""
Python Type Hints Examples
This module demonstrates various ways to use type hints in Python.

Type hints were introduced in Python 3.5 (PEP 484)
and have become increasingly important.
They provide several benefits:
1. Better code documentation
2. Enhanced IDE support
3. Static type checking with tools like mypy
4. Improved code maintenance
"""

from dataclasses import dataclass
from datetime import datetime
from typing import (
    Callable,
    Dict,
    Final,
    Generic,
    List,
    Literal,
    Optional,
    Protocol,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
    overload,
)


# 1. Basic Type Hints
def calculate_age(birth_year: int) -> int:
    """Basic type hints for parameters and return value"""
    current_year = datetime.now().year
    return current_year - birth_year


# 2. Multiple Types (Union)
def process_id(identifier: Union[int, str]) -> str:
    """Accept either int or str as input"""
    return str(identifier).strip()


# 3. Optional Parameters
def greet(name: Optional[str] = None) -> str:
    """Optional parameter using Optional[str] (same as Union[str, None])"""
    if name is None:
        return "Hello, Guest!"
    return f"Hello, {name}!"


# 4. Collections
def process_numbers(numbers: List[int]) -> Dict[str, List[int]]:
    """Type hints with collections"""
    return {
        "original": numbers,
        "doubled": [n * 2 for n in numbers],
        "squared": [n**2 for n in numbers],
    }


# 5. Tuples with Fixed Size
def get_coordinates() -> Tuple[float, float]:
    """Return a tuple with a fixed number of elements"""
    return (40.7128, -74.0060)  # New York coordinates


# 6. Callable Types
def apply_operation(x: int, operation: Callable[[int], int]) -> int:
    """Function that takes another function as parameter"""
    return operation(x)


# 7. Generic Types with TypeVar
T = TypeVar("T")


class Stack(Generic[T]):
    """Generic class that can work with any type"""

    def __init__(self) -> None:
        self.items: List[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> Optional[T]:
        return self.items.pop() if self.items else None


# 8. TypedDict for Dictionary Structure
class UserDict(TypedDict):
    """TypedDict for specifying dictionary structure"""

    id: int
    name: str
    email: str
    active: bool


def create_user(data: UserDict) -> UserDict:
    return data


# 9. Literal Types
def set_log_level(level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]) -> None:
    """Function that only accepts specific string literals"""
    print(f"Setting log level to: {level}")


# 10. Final for Constants
MAX_ATTEMPTS: Final[int] = 3


# 11. Protocol for Duck Typing
class Drawable(Protocol):
    """Protocol defining what makes something drawable"""

    def draw(self) -> None:
        ...


def render(entity: Drawable) -> None:
    """Accept any object that has a draw method"""
    entity.draw()


# 12. Type Aliases
Vector = List[float]
Matrix = List[Vector]


def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    """Example using type aliases"""
    # Implementation omitted for brevity
    return [[0.0]]


# 13. Dataclasses with Types
@dataclass
class Point:
    """Dataclass with type hints"""

    x: float
    y: float
    label: Optional[str] = None


# 14. Function Overloading
@overload
def process_data(data: str) -> str:
    ...


@overload
def process_data(data: bytes) -> bytes:
    ...


def process_data(data: Union[str, bytes]) -> Union[str, bytes]:
    """Function with multiple signatures"""
    if isinstance(data, str):
        return data.upper()
    return data.upper()


def run_type_hint_examples() -> None:
    """Run examples demonstrating type hints"""
    print("\n=== Type Hints Examples ===")

    # Basic type hints
    age = calculate_age(1990)
    print(f"Age: {age}")

    # Union types
    id_result = process_id(123)
    print(f"Processed ID: {id_result}")

    # Optional parameters
    print(greet())
    print(greet("Alice"))

    # Collections
    numbers_result = process_numbers([1, 2, 3])
    print(f"Processed numbers: {numbers_result}")

    # Generic Stack
    stack: Stack[int] = Stack()
    stack.push(1)
    stack.push(2)
    print(f"Popped from stack: {stack.pop()}")

    # TypedDict
    user: UserDict = {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "active": True,
    }
    print(f"Created user: {create_user(user)}")

    # Literal types
    set_log_level("DEBUG")

    # Dataclass
    point = Point(x=10.0, y=20.0, label="Center")
    print(f"Point: {point}")


if __name__ == "__main__":
    run_type_hint_examples()
