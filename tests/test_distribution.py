from nose.tools import assert_equal
from craftai.interpreter_v2 import InterpreterV2

def test_regression_mean():
  array = [[10], [20], [30]]
  sizes = [1, 1, 1]
  res = list(InterpreterV2.compute_mean(array, sizes))
  assert_equal(res, [20.0])

  array = [[10], [20], [30]]
  sizes = [0, 0, 1000]
  res = list(InterpreterV2.compute_mean(array, sizes))
  assert_equal(res, [30.0])

def test_classification_probabilities():
  array = [[0.1, 0.2, 0.7],
           [0.1, 0.2, 0.7],
           [0.1, 0.2, 0.7]]
  sizes = [1, 1, 1]
  res = list(InterpreterV2.compute_mean(array, sizes))
  assert_equal(res, [0.1, 0.2, 0.7])

  array = [[1.0, 0.0, 0.0],
           [0.0, 1.0, 0.0],
           [0.0, 0.0, 1.0]]
  sizes = [1, 1, 1]
  res = list(InterpreterV2.compute_mean(array, sizes))
  assert_equal(res, [1/3., 1/3., 1/3.])
