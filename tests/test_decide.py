import json
import os
import unittest

from . import settings

from craftai.client import CraftAIClient
from craftai.time import Time
from craftai.helpers import dict_depth
from craftai import errors as craft_err

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
                    decision = self.client.decide(tree, exp_context, t)
                    print("decision: ", decision)
                    print("expectation: ", expectation.get("output"))
                    self.assertEqual(
                        dict_depth(decision),
                        dict_depth(expectation["output"]))
            print("--------------------------")
