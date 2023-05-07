def compound(a: float, b: float):
  """(1 + a/100)*(1 + b/100) - 1 을 구한다."""
  return a + b + a * b / 100
