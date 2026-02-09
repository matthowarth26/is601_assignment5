"""
tests/test_operations.py

This module contains unit tests for the Operations class, which performs basic arithmetic
operations such as addition, subtraction, multiplication, and division. By utilizing
parameterized tests with pytest, we can efficiently test multiple scenarios with 
different input values, ensuring that each metho behaves as expected under various conditions.

Parameterized test help in reducing code duplication and enhancing test coverage by allowing 
the same test logic to run with different inputs and expected outcomes. 

Prerequisites:
- Understanding of Python classes and methods.
- Basic knowledge of pytest framework.
"""

import pytest # Import the pytest framework for writing and running tests 
from typing import Union # Import Union for type hinting multiple possible types 
from app.operations import Operations # Import the Operations class from the operations module 

# Define a type alias for numbers that can be either int or float
Number = Union[int, float]

# ---------------------------------------------
# Unit tests for the 'addition' method
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected", 
    [
        (2, 3, 5),          # Test adding two positive integers
        (0, 0, 0),          # Test adding two zeros
        (-1, 1, 0),         # Test adding a negative and a positive integer
        (2.5, 3.5, 6.0),    # Test adding two positive floats
        (-2.5, 3.5, 1.0),   # Test adding a negative float and a positive float  
    ],
    ids=[
        "add_two_positive_integers",
        "add_two_zeros",
        "add_negatives_and_positive_integers",
        "add_two_positive_floats",
        "add_negative_float_and_positive_float"
    ]
)

def test_addition(a: Number, b: Number, expected: Number) -> None:
    """
    Test the 'addition' method of the Operations class with various input combinations.

    This parameterized test verifies that the 'addition' method correctly adds two numbers, 
    whether they are positive, negative, integers, or floats. By using parameterization, 
    we can efficiently test multiple scenarios without redundant code.

    Parameters:
    - a (Number): The first number to add
    - b (Number): The second number to add 
    - expected (Number): The expected result of addition

    Steps:
    1. Call the 'addition' method with arguments 'a' and 'b' 
    2. Assert that the result is equal to the 'expected' 

    Example: 
    >>> test_addition(2, 3, 5)
    >>> test_addition(-1, 1, 0)
    """
    # Create an instance of the Operations class

    # Call the 'addition' method with the provided arguments 
    result = Operations.addition(a, b)

    # Assert that the results of addition (a, b) matches the expected value 
    assert result == expected, f"Expected addition({a},{b}) to be {expected}, but got {result}"

# ---------------------------------------------
# Unit tests for the 'subtraction' method
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected", 
    [
        (5, 3, 2),           # Test subtracting a smaller positive integer from a larger one 
        (0, 0, 0),           # Test subracting two zeros
        (-5, -3, -2),        # Test subtracting a negative integer from another negative integer 
        (10.5, 5.5, 5.0),    # Test subtracting two positive floats
        (-10.5, -5.5, -5.0), # Test subtracting two negative floats 
    ],
    ids=[
        "subtract_smaller_positive_integer_from_larger",
        "subtract_two_zeros",
        "subtract_negative_integer_from_negative_integer",
        "subtract_two_positive_floats",
        "subtract_two_negative_floats"
    ]
)

def test_subtraction(a: Number, b: Number, expected: Number) -> None:
    """
    Test the 'subtraction' method of the Operations class with various input combinations.

    This parameterized test verifies that the 'subtraction' method correctly subtracts the 
    second number from the first, handling both positive and negative values, as well as 
    integers and floats. Parameterization allows for comprehensive testing of multiple cases. 

    Parameters:
    - a (Number): The number from which to subtract
    - b (Number): The number to subtract 
    - expected (Number): The expected result of subtraction 

    Steps:
    1. Call the 'subtraction' method with arguments 'a' and 'b' 
    2. Assert that the result is equal to the 'expected' 

    Example: 
    >>> test_subtraction(5, 3, 2)
    >>> test_subtraction(-5, -3, -2)
    """
    # Create an instance of the Operations class

    # Call the 'subtraction' method with the provided arguments 
    result = Operations.subtraction(a, b)

    # Assert that the results of subtraction (a, b) matches the expected value 
    assert result == expected, f"Expected subtraction({a},{b}) to be {expected}, but got {result}"

# ---------------------------------------------
# Unit tests for the 'multiplication' method
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected", 
    [
        (2, 3, 6),           # Test multiplying two positive integers
        (0, 10, 0),          # Test multiplying zero with a positive integer
        (-2, -3, 6),         # Test multiplying two negative integers
        (2.5, 4.0, 10.0),    # Test multiplying two positive floats 
        (-2.5, 4.0, -10.0),  # Test multiplying a negative float with a positive float  
    ],
    ids=[
        "multiply_two_positive_integers",
        "multiply_zero_with_positive_integer",
        "multiply_two_negative_integers",
        "multiply_two_positive_floats",
        "multiply_negative_float_with_positive_float"
    ]
)

def test_multiplication(a: Number, b: Number, expected: Number) -> None:
    """
    Test the 'multiplication' method of the Operations class with various input combinations.

    This parameterized test verifies that the 'multiplication' method correctly multiplies two numbers,
    handling both positive and negative values, as well as integers and floats. Parameterization 
    enables efficient testing of multiple scenarios in a concise manner. 

    Parameters:
    - a (Number): The first number to multiply 
    - b (Number): The second number to multiply 
    - expected (Number): The expected result of multiplication  

    Steps:
    1. Call the 'multiplication' method with arguments 'a' and 'b' 
    2. Assert that the result is equal to the 'expected' 

    Example: 
    >>> test_multiplication(2, 3, 6)
    >>> test_multiplication(-2, -3, 6)
    """
    # Create an instance of the Operations class

    # Call the 'multiplication' method with the provided arguments 
    result = Operations.multiplication(a, b)

    # Assert that the results of multiplcation (a, b) matches the expected value 
    assert result == expected, f"Expected multiplication({a},{b}) to be {expected}, but got {result}"

# ---------------------------------------------
# Unit tests for the 'division' method
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected", 
    [
        (6, 3, 2.0),          # Test dividing two positive integers
        (-6, -3, 2.0),        # Test dividing two negative integers 
        (6.0, 3.0, 2.0),      # Test dividing two positive floats 
        (-6.0, 3.0, -2.0),    # Test dividing a negative float by a positive float 
        (0, 5, 0.0),          # Test dividing zero by a positive integer 
    ],
    ids=[
        "divide_two_positive_integers", 
        "divide_two_negative_integers", 
        "divide_two_positive_floats", 
        "divide_negative_float_by_positive_float", 
        "divide_zero_by_positive_integer"
    ]
)

def test_division(a: Number, b: Number, expected: float) -> None: 
    """
    Test the 'division' method of the Operations class with various input combinations.

    This parameterized test verifies that the 'division' method correctly divides the first
    number by the second, handling both positive and negative values, as well as integers
    and floats. Parameterization allows for efficient and comprehensive testing across multiple cases.  

    Parameters:
    - a (Number): The dividend 
    - b (Number): The divisor 
    - expected (Number): The expected result of division   

    Steps:
    1. Call the 'division' method with arguments 'a' and 'b' 
    2. Assert that the result is equal to the 'expected' 

    Example: 
    >>> test_division(6, 3, 2.0)
    >>> test_division(-6, 3, -2.0)
    """
    # Create an instance of the Operations class

    # Call the 'division' method with the provided arguments 
    result = Operations.division(a, b)

    # Assert that the results of multiplcation (a, b) matches the expected value 
    assert result == expected, f"Expected division({a},{b}) to be {expected}, but got {result}"  

# ---------------------------------------------
# Negative Test Case: Division by Zero 
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b", 
    [
        (1, 0),         # Test dividing by zero with positive dividend 
        (-1, 0),        # Test dividing by zero with negative dividend 
        (0, 0),         # Test dividing zero by zero 
    ],
    ids=[
        "divide_positive_dividend_by_zero", 
        "divide_negative_dividend_by_zero", 
        "divide_zero_by_zero", 
    ]
)

def test_division_by_zero(a: Number, b: Number) -> None: 
    """
    Test the 'division' method of the Operations class when dividing by zero. 

    This negative test case verifies that attempting to divide by zero raises a ValueError
    with the appropriate error message. It ensures that the application correctly handles 
    invalid operations and provides meaningful feedback to th user. 

    Parameters:
    - a (Number): The dividend 
    - b (Number): The divisor (zero in this case)

    Steps:
    1. Attempt to call the 'division' method with arguments 'a' and 'b', which should raise a ValueError
    2. Use pytest's 'raises' context manager to catch the expected exception 
    3. Assert that the error message contains "Division by zero is not allowed." 

    Example: 
    >>> test_division_by_zero(1, 0)
    >>> test_division_by_zero(-1, 0)
    """
    # Create an instance of the Operations class

    # Use pytest's context manager to check for a ValueError when dividing by zero
    with pytest.raises(ValueError, match="Division by zero is not allowed.") as excinfo:
        # Attempt to divide 'a' by 'b', which should raise a ValueError
        Operations.division(a, b)

    # Assert that the exception message contains the expected error message
    assert "Division by zero is not allowed." in str(excinfo.value), \
        f"Expected error message 'Division by zero is not allowed.', but got '{excinfo.value}'"  