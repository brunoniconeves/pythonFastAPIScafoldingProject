"""
Common Algorithm Questions in Python Interviews
"""


def reverse_string(s: str) -> str:
    """
    Reverse a string without using built-in reversed() or slice notation
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    return "".join([s[i] for i in range(len(s) - 1, -1, -1)])


def is_palindrome(s: str) -> bool:
    """
    Check if a string is palindrome (reads same forwards and backwards)
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    s = "".join(c.lower() for c in s if c.isalnum())
    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1

    return True


def find_first_duplicate(arr: list) -> int:
    """
    Find first duplicate number in an array
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen = set()
    for num in arr:
        if num in seen:
            return num
        seen.add(num)
    return -1


def binary_search(arr: list, target: int) -> int:
    """
    Binary search implementation
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def merge_sorted_arrays(arr1: list, arr2: list) -> list:
    """
    Merge two sorted arrays
    Time Complexity: O(n + m)
    Space Complexity: O(n + m)
    """
    result = []
    i = j = 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1

    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result


def find_missing_number(arr: list) -> int:
    """
    Find missing number in array of 1 to n
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    n = len(arr) + 1
    expected_sum = (n * (n + 1)) // 2
    actual_sum = sum(arr)
    return expected_sum - actual_sum


def is_balanced_parentheses(s: str) -> bool:
    """
    Check if parentheses are balanced
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack.pop() != pairs[char]:
                return False

    return len(stack) == 0


def find_two_sum(arr: list, target: int) -> tuple:
    """
    Find two numbers that add up to target
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return (-1, -1)


# Example usage
if __name__ == "__main__":
    # Test reverse string
    print(f"Reverse 'hello': {reverse_string('hello')}")

    # Test palindrome
    print(
        f"Is 'A man, a plan, a canal: Panama' palindrome? "
        f"{is_palindrome('A man, a plan, a canal: Panama')}"
    )

    # Test first duplicate
    print(f"First duplicate in [1,2,3,2,1]: {find_first_duplicate([1,2,3,2,1])}")

    # Test binary search
    sorted_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"Binary search for 5 in {sorted_array}: {binary_search(sorted_array, 5)}")

    # Test merge sorted arrays
    arr1 = [1, 3, 5]
    arr2 = [2, 4, 6]
    print(f"Merged {arr1} and {arr2}: {merge_sorted_arrays(arr1, arr2)}")

    # Test find missing number
    print(f"Missing number in [1,2,4,5]: {find_missing_number([1,2,4,5])}")

    # Test balanced parentheses
    print(f"Is '({[]})' balanced? {is_balanced_parentheses('({[]})')}")

    # Test two sum
    print(f"Two numbers adding to 9 in [2,7,11,15]: {find_two_sum([2,7,11,15], 9)}")
