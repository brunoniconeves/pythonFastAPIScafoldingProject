"""
Python Magic Methods (Dunder Methods) Examples

Magic methods are special methods surrounded by double underscores (__).
They allow you to define how your objects behave in response to:
- Object creation/initialization
- Operations (addition, subtraction, etc.)
- String representation
- Context management
- And more...
"""


class BankAccount:
    """
    A class demonstrating common magic methods
    """

    # 1. Object Lifecycle Methods
    def __init__(self, owner: str, balance: float = 0.0):
        """Constructor - Called when creating a new object"""
        self.owner = owner
        self.balance = balance
        print(f"__init__: Creating account for {owner}")

    def __del__(self):
        """Destructor - Called when object is garbage collected"""
        print(f"__del__: Deleting account for {self.owner}")

    # 2. String Representation Methods
    def __str__(self):
        """Informal string representation - for users"""
        return (
            f"Bank account belonging to {self.owner} with balance ${self.balance:.2f}"
        )

    def __repr__(self):
        """Formal string representation - for developers"""
        return f"BankAccount(owner='{self.owner}', balance={self.balance})"

    # 3. Comparison Methods
    def __eq__(self, other):
        """Equal to - Called when using =="""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.balance == other.balance

    def __lt__(self, other):
        """Less than - Called when using <"""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.balance < other.balance

    def __gt__(self, other):
        """Greater than - Called when using >"""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.balance > other.balance

    # 4. Numeric Operation Methods
    def __add__(self, other):
        """Addition - Called when using +"""
        if isinstance(other, (int, float)):
            return BankAccount(self.owner, self.balance + other)
        if isinstance(other, BankAccount):
            new_balance = self.balance + other.balance
            new_owner = f"{self.owner} & {other.owner}"
            return BankAccount(new_owner, new_balance)
        return NotImplemented

    def __sub__(self, other):
        """Subtraction - Called when using -"""
        if isinstance(other, (int, float)):
            return BankAccount(self.owner, self.balance - other)
        return NotImplemented

    # 5. Container Methods
    def __len__(self):
        """Length - Called when using len()"""
        # Return number of whole dollars
        return int(self.balance)

    def __bool__(self):
        """Boolean value - Called when using bool()"""
        return self.balance > 0

    # 6. Context Manager Methods
    def __enter__(self):
        """Enter context - Called in 'with' statement"""
        print(f"__enter__: Starting transaction for {self.owner}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context - Called when leaving 'with' statement"""
        print(f"__exit__: Ending transaction for {self.owner}")
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return False  # Don't suppress exceptions

    # 7. Callable Method
    def __call__(self, amount: float):
        """Make object callable - Called when using object as function"""
        self.balance += amount
        return self.balance


def demonstrate_magic_methods():
    """
    Demonstrates the usage of magic methods
    """
    print("\n=== Magic Methods Demonstration ===")

    # 1. Object Creation and String Representation
    print("\n1. Creating objects and string representation:")
    account1 = BankAccount("Alice", 1000)
    account2 = BankAccount("Bob", 2000)

    print(f"str(account1): {account1!s}")  # Uses __str__
    print(f"repr(account1): {account1!r}")  # Uses __repr__

    # 2. Comparison Operations
    print("\n2. Comparing accounts:")
    print(f"account1 == account2: {account1 == account2}")  # Uses __eq__
    print(f"account1 < account2: {account1 < account2}")  # Uses __lt__
    print(f"account1 > account2: {account1 > account2}")  # Uses __gt__

    # 3. Numeric Operations
    print("\n3. Numeric operations:")
    # Adding two accounts
    combined = account1 + account2
    print(f"Combined account: {combined}")

    # Adding money to account
    rich_account = account1 + 500
    print(f"After adding 500: {rich_account}")

    # Subtracting money
    reduced_account = account1 - 200
    print(f"After subtracting 200: {reduced_account}")

    # 4. Container Operations
    print("\n4. Container operations:")
    print(f"len(account1): {len(account1)}")  # Uses __len__
    print(f"bool(account1): {bool(account1)}")  # Uses __bool__

    # 5. Context Manager
    print("\n5. Context manager:")
    with account1 as acc:
        print(f"Inside context manager with balance: {acc.balance}")
        # Simulate transaction
        acc.balance += 100

    # 6. Callable Object
    print("\n6. Using object as function:")
    new_balance = account1(500)  # Add 500 to balance
    print(f"After calling account1(500): {new_balance}")


if __name__ == "__main__":
    demonstrate_magic_methods()
