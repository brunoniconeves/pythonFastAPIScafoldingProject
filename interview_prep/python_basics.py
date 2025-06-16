"""
Common Python Interview Concepts with Examples
Run specific examples using command line arguments:
python python_basics.py --help
python python_basics.py --all
python python_basics.py --list-comp --decorator --context-manager
"""

import argparse
from typing import Callable


# 1. List Comprehension vs Generator Expression
def list_comp_vs_gen():
    """
    Demonstrates the differences between list comprehensions and generator expressions
    """
    # List comprehension - creates list in memory
    squares_list = [x * x for x in range(10)]

    # Generator expression - generates values on demand
    squares_gen = (x * x for x in range(10))

    # Demonstrate reusability
    print("\nReusability Demonstration:")
    # List can be reused
    print(f"List sum: {sum(squares_list)}")
    print(f"List max: {max(squares_list)}")  # List still has all values

    # Generator gets exhausted
    print(f"Generator sum: {sum(squares_gen)}")
    try:
        print(f"Generator max: {max(squares_gen)}")  # Generator is now empty
    except ValueError as e:
        print(f"Generator is exhausted: {e}")

    # Demonstrate memory efficiency
    big_list = list(range(1000000))  # Creates all numbers in memory
    big_gen = (x for x in range(1000000))  # Creates generator object only

    print("\nMemory Usage Demonstration:")
    print(f"List size: {len(big_list)}")
    print(f"Generator object: {big_gen}")  # Shows generator object only

    # Demonstrate processing efficiency
    print("\nProcessing Large Data:")
    # Process first 5 items from a new generator
    large_gen = (x for x in range(1000000))
    for i, num in enumerate(large_gen):
        if i >= 5:
            break
        print(f"Generated number {i}: {num}")

    return squares_list, squares_gen


# 2. Decorator Example
def timing_decorator(func):
    from time import time

    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"{func.__name__} took {end-start} seconds")
        return result

    return wrapper


@timing_decorator
def slow_function():
    import time

    time.sleep(1)
    return "Done"


# 3. Context Manager
class DatabaseConnection:
    def __enter__(self):
        print("Opening database connection")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection")
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        return False  # Don't suppress exceptions


# 4. Iterator Example
class Fibonacci:
    def __init__(self, limit):
        self.limit = limit
        self.n1 = 0
        self.n2 = 1
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.limit:
            raise StopIteration

        if self.count == 0:
            self.count += 1
            return self.n1
        elif self.count == 1:
            self.count += 1
            return self.n2
        else:
            result = self.n1 + self.n2
            self.n1 = self.n2
            self.n2 = result
            self.count += 1
            return result


# 5. Property Decorator
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        import math

        return math.pi * self._radius**2


# 6. Multiple Inheritance and MRO (Method Resolution Order)
class Animal:
    def speak(self):
        return "Some sound"


class Flyable:
    def fly(self):
        return "Flying"


class Bird(Animal, Flyable):
    def speak(self):
        return "Chirp"


# 7. Exception Handling with Custom Exception
class ValidationError(Exception):
    pass


def divide_numbers(a, b):
    try:
        if b == 0:
            raise ValidationError("Cannot divide by zero")
        return a / b
    except ValidationError as e:
        return str(e)
    except TypeError:
        return "Please provide numbers only"
    finally:
        print("Division attempt completed")


# 8. Lambda and Higher Order Functions
def apply_operation(x, y, operation):
    return operation(x, y)


def add(x, y):
    x + y


def multiply(x, y):
    x * y


def run_list_comprehension_example():
    """Run and display list comprehension vs generator example"""
    lst, gen = list_comp_vs_gen()
    print("\n=== List Comprehension vs Generator ===")
    print(f"List: {lst}")
    print(f"Generator: {list(gen)}")


def run_decorator_example():
    """Run and display decorator example"""
    print("\n=== Decorator Example ===")
    result = slow_function()
    print(f"Result: {result}")


def run_context_manager_example():
    """Run and display context manager example"""
    print("\n=== Context Manager Example ===")
    with DatabaseConnection():
        print("Doing something with the database")


def run_iterator_example():
    """Run and display iterator example"""
    print("\n=== Iterator Example ===")
    fib = Fibonacci(5)
    print("Fibonacci sequence:")
    for num in fib:
        print(num)


def run_property_example():
    """Run and display property decorator example"""
    print("\n=== Property Example ===")
    circle = Circle(5)
    print(f"Circle area: {circle.area}")
    try:
        circle.radius = -1
    except ValueError as e:
        print(f"Validation working: {e}")


def run_inheritance_example():
    """Run and display multiple inheritance example"""
    print("\n=== Multiple Inheritance Example ===")
    bird = Bird()
    print(f"Bird speaks: {bird.speak()}")
    print(f"Bird can: {bird.fly()}")
    print(f"Method Resolution Order: {[c.__name__ for c in Bird.__mro__]}")


def run_exception_example():
    """Run and display exception handling example"""
    print("\n=== Exception Handling Example ===")
    print(f"10/2 = {divide_numbers(10, 2)}")
    print(f"10/0 = {divide_numbers(10, 0)}")
    print(f"'10'/'2' = {divide_numbers('10', '2')}")


def run_lambda_example():
    """Run and display lambda and higher order functions example"""
    print("\n=== Lambda and Higher Order Functions Example ===")
    print(f"Add: {apply_operation(5, 3, add)}")
    print(f"Multiply: {apply_operation(5, 3, multiply)}")

    # Additional example with custom lambda
    def power(x, y):
        x**y

    print(f"Power: {apply_operation(5, 3, power)}")


def get_available_examples() -> dict[str, tuple[Callable, str]]:
    """
    Returns a dictionary of available examples with their functions and descriptions
    """
    return {
        "list-comp": (
            run_list_comprehension_example,
            "List comprehension vs Generator expression example",
        ),
        "decorator": (run_decorator_example, "Decorator pattern example"),
        "context-manager": (run_context_manager_example, "Context manager example"),
        "iterator": (run_iterator_example, "Iterator pattern with Fibonacci example"),
        "property": (run_property_example, "Property decorator example"),
        "inheritance": (run_inheritance_example, "Multiple inheritance example"),
        "exception": (run_exception_example, "Exception handling example"),
        "lambda": (run_lambda_example, "Lambda and higher order functions example"),
    }


def setup_argparse() -> argparse.ArgumentParser:
    """
    Set up command line argument parser
    """
    examples = get_available_examples()

    parser = argparse.ArgumentParser(
        description="Python Interview Concepts Examples",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("--all", action="store_true", help="Run all examples")

    for arg, (_, desc) in examples.items():
        parser.add_argument(f"--{arg}", action="store_true", help=desc)

    return parser


if __name__ == "__main__":
    parser = setup_argparse()
    args = parser.parse_args()
    examples = get_available_examples()

    # If no arguments provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        exit(0)

    # Run selected examples
    for arg, (func, _) in examples.items():
        if args.all or getattr(args, arg.replace("-", "_")):
            func()
