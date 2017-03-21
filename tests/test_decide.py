import json
import os
import unittest

from . import settings

from craftai.client import CraftAIClient
from craftai.time import Time
from craftai.helpers import dict_depth
from craftai import errors as craft_err
from craftai.interpreter import Interpreter

HERE = os.path.abspath(os.path.dirname(__file__))

# Assuming we are the test folder and the folder hierarchy is correctly
# constructed
EXPECS_DIR = os.path.join(HERE, "data", "interpreter", "expectations")
TREES_DIR = os.path.join(HERE, "data", "interpreter", "trees")


class TestDecide(unittest.TestCase):
    """Checks that given a certain tree and context, the decision matches what
    is expected."""
    @classmethod
    def setUpClass(self):
        self.maxDiff = None
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        self.tree_files = os.listdir(TREES_DIR)

    def test_decide(self):
        for tree_file in self.tree_files:
            print("test file: ", tree_file)
            # Loading the json tree
            with open(os.path.join(TREES_DIR, tree_file)) as f:
                tree = json.load(f)
            # Loading the expectations for this tree
            with open(os.path.join(EXPECS_DIR, tree_file)) as f:
                expectations = json.load(f)

            for expectation in expectations:
                # Preparing decide() arguments
                exp_context = expectation["context"]
                timestamp = None
                exp_time = expectation.get("time")
                t = Time(exp_time["t"], exp_time["tz"]) if exp_time else {}

                if expectation.get("error"):
                    self.assertRaises(
                        craft_err.CraftAIDecisionError,
                        self.client.decide,
                        tree,
                        exp_context,
                        timestamp)
                    print("Successfully raises CraftAIDecisionError.")
                else:
                    print(expectation)
                    decision = self.client.decide(tree, exp_context, t)
                    decision_output = decision["decision"]
                    expectation_output = expectation["output"]["decision"]
                    for x in expectation_output.keys():
                        self.assertEqual(expectation_output[x], decision_output[x])
            print("--------------------------")

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

        # Case 1:
        # - we do not provide a Time object while properties in configuration need to be generated from it
        # - we do not provide those properties directly in the context
        state = { "car": "Renault", "day_of_week": 2 }
        self.assertRaises(
            craft_err.CraftAIDecisionError,
            Interpreter._rebuild_context,
            configuration,
            state)
        print("Successfully raises CraftAIDecisionError.")

        # Case 2:
        # - we do provide a Time object while it's needed
        # - in the context, we set a value that should be generated if not provided,
        #   but we provide it and we don't want it to be replaced by generated value
        state = { "car": "Renault", "day_of_week": 2, "timezone": "+02:00" }
        time = Time(1489998174, "+01:00")
        expected_context = {
            "car": "Renault",
            "day_of_week": 2,
            "month_of_year": 3,
            "timezone": "+02:00" # must not be replaced by +01:00
        }
        rebuilt_context = Interpreter._rebuild_context(configuration, state, time)
        for x in expected_context.keys():
            self.assertEqual(rebuilt_context[x], expected_context[x])

        # Case 3:
        # - we provide none of the properties that should be generated
        state = { "car": "Renault", "day_of_week": 2 }
        time = Time(1489998174, "+01:00")
        rebuilt_context = Interpreter._rebuild_context(configuration, state, time)
        expected_context = {
            "car": "Renault",
            "day_of_week": 2,
            "month_of_year": 3,
            "timezone": "+01:00"
        }
        for x in expected_context.keys():
            self.assertEqual(rebuilt_context[x], expected_context[x])
