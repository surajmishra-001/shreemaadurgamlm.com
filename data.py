def factorial(n):
  """
  This function calculates the factorial of a non-negative integer.

  Args:
      n (int): The non-negative integer for which to calculate the factorial.

  Returns:
      int: The factorial of n.

  Raises:
      ValueError: If n is negative.
  """

  if n < 0:
    raise ValueError("n must be non-negative")
  elif n == 0:
    return 1
  else:
    return n * factorial(n-1)

# Example usage
try:
  result = factorial(15)
  print(f"The factorial of 5 is: {result}")
except ValueError as e:
  print(f"Error: {e}")
