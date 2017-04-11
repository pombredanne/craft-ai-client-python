import json
import os
import unittest

from craftai import errors as craft_err
from craftai.client import CraftAIClient
from craftai.interpreter import Interpreter
from craftai.time import Time

from . import settings

HERE = os.path.abspath(os.path.dirname(__file__))

# Assuming we are the test folder and the folder hierarchy is correctly
# constructed
EXPECS_DIR = os.path.join(HERE, "data", "interpreter", "expectations")
TREES_DIR = os.path.join(HERE, "data", "interpreter", "trees")


class TestDecide(unittest.TestCase):
  """Checks that given a certain tree and context, the decision matches what
  is expected."""
  @classmethod
  def setUpClass(cls):
    cls.maxDiff = None
    cls.client = CraftAIClient(settings.CRAFT_CFG)

  def setUp(self):
    self.tree_files = os.listdir(TREES_DIR)

  def test_decide(self):
    for tree_file in self.tree_files:
      # Loading the json tree
      with open(os.path.join(TREES_DIR, tree_file)) as file:
        tree = json.load(file)
      # Loading the expectations for this tree
      with open(os.path.join(EXPECS_DIR, tree_file)) as file:
        expectations = json.load(file)

      for expectation in expectations:
        # Preparing decide() arguments
        exp_context = expectation["context"]
        timestamp = None
        exp_time = expectation.get("time")
        time = Time(exp_time["t"], exp_time["tz"]) if exp_time else {}

        if expectation.get("error"):
          self.assertRaises(
            craft_err.CraftAiDecisionError,
            self.client.decide,
            tree,
            exp_context,
            timestamp)
        else:
          decision = self.client.decide(tree, exp_context, time)
          decision_output = decision["output"]
          expectation_output = expectation["output"]["output"]
          for output in list(expectation_output.keys()):
            self.assertEqual(expectation_output[output], decision_output[output])

  def test__rebuild_context(self):
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
    self.assertRaises(
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
      self.assertEqual(rebuilt_context[output], expected_context[output])
