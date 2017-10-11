import json
import os

from craftai import Client, Interpreter, Time, errors as craft_err
from nose.tools import assert_raises, assert_equal

from . import settings

#pylint: disable=E1101
assert_equal.__self__.maxDiff = None
#pylint: enable=E1101

HERE = os.path.abspath(os.path.dirname(__file__))

# Assuming we are the test folder and the folder hierarchy is correctly
# constructed
EXPECS_DIR = os.path.join(HERE, "data", "interpreter", "expectations")
TREES_DIR = os.path.join(HERE, "data", "interpreter", "trees")

CLIENT = Client(settings.CRAFT_CFG)

def interpreter_tests_generator():
  tree_files = os.listdir(TREES_DIR)
  for tree_file in tree_files:
    # Loading the json tree
    with open(os.path.join(TREES_DIR, tree_file)) as f:
      tree = json.load(f)
    # Loading the expectations for this tree
    with open(os.path.join(EXPECS_DIR, tree_file)) as f:
      expectations = json.load(f)

    for expectation in expectations:
#pylint: disable=W0108
      test_fn = lambda t, e: check_expectation(t, e)
#pylint: enable=W0108

      test_fn.description = tree_file + " - " + expectation["title"]
      interpreter_tests_generator.compat_func_name = test_fn.description

      yield test_fn, tree, expectation

def check_expectation(tree, expectation):
  exp_context = expectation["context"]
  timestamp = None
  exp_time = expectation.get("time")
  time = Time(exp_time["t"], exp_time["tz"]) if exp_time else {}

  if expectation.get("error"):
    with assert_raises(craft_err.CraftAiDecisionError) as context_manager:
      CLIENT.decide(tree, exp_context, timestamp)

    exception = context_manager.exception
    assert_equal(exception.message, expectation["error"]["message"].encode("utf8"))
  else:
    expected_decision = expectation["output"]
    decision = CLIENT.decide(tree, exp_context, time)
    assert_equal(decision, expected_decision)

def test_rebuild_context():
  configuration = {
    "context": {
      "car": {
        "type": "enum"
      },
      "speed": {
        "type": "continuous"
      },
      "day_of_week": {
        "type": "day_of_week",
        "is_generated": False
      },
      "month_of_year": {
        "type": "month_of_year"
      },
      "timezone": {
        "type": "timezone"
      }
    },
    "output": ["speed"],
    "time_quantum": 500
  }

#pylint: disable=W0212

  # Case 1:
  # - don't provide a Time object while properties in configuration need to be generated from it
  # - don't provide those properties directly in the context
  state = {"car": "Renault", "day_of_week": 2}
  assert_raises(
    craft_err.CraftAiDecisionError,
    Interpreter._rebuild_context,
    configuration,
    state)

  # Case 2:
  # - provide none of the properties that should be generated
  state = {"car": "Renault", "day_of_week": 2}
  time = Time(1489998174, "+01:00")
  rebuilt_context = Interpreter._rebuild_context(configuration, state, time)
  expected_context = {
    "car": "Renault",
    "day_of_week": 2,
    "month_of_year": 3,
    "timezone": "+01:00"
  }

#pylint: enable=W0212

  for output in expected_context:
    assert_equal(rebuilt_context[output], expected_context[output])
