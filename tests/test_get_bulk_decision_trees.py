import unittest
import six
import random
import semver

from nose.tools import nottest
from craftai import Client, errors as craft_err

from . import settings
from .data import valid_data
from .data import invalid_data

VALID_L_CFG = valid_data.VALID_LARGE_CONFIGURATION
VALID_L_BATCH_DURATION = VALID_L_CFG["learning_period"] * 4
VALID_L_ENUM_VALUES = ["CYAN", "MAGENTA", "YELLOW", "BLACK"]

class TestGetDecisionTreeSuccess(unittest.TestCase):
  """Checks that the client succeeds when getting
  an/multiple decision tree(s) with OK input"""

  @classmethod
  def setUpClass(cls):
    cls.client = Client(settings.CRAFT_CFG)
    cls.agent_id1 = valid_data.VALID_ID  + "_" + settings.RUN_ID
    cls.agent_id2 = valid_data.VALID_ID_TWO  + "_" + settings.RUN_ID
    cls.VALID_L_OPERATIONS = [
      [
        {
          "timestamp": batch_offset * VALID_L_BATCH_DURATION + operation_offset,
          "context": {
            "e1": random.choice(VALID_L_ENUM_VALUES),
            "e2": random.choice(VALID_L_ENUM_VALUES),
            "e3": random.choice(VALID_L_ENUM_VALUES),
            "e4": random.choice(VALID_L_ENUM_VALUES),
            "c1": random.uniform(-12, 12),
            "c2": random.uniform(-12, 12),
            "c3": random.uniform(-12, 12),
            "c4": random.uniform(-12, 12),
            "tz": "CET"
          }
        }
        for operation_offset in range(0, VALID_L_BATCH_DURATION, 1000)
      ]
    for batch_offset in range(0, 60)
    ]

  def setUp(self):
    # Makes sure that no agent with the same ID already exists
    self.client.delete_agent(self.agent_id1)
    self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id1)
    self.client.add_operations(self.agent_id1, valid_data.VALID_OPERATIONS_SET)

    self.client.delete_agent(self.agent_id2)
    self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id2)
    self.client.add_operations(self.agent_id2, valid_data.VALID_OPERATIONS_SET)

  def clean_up_agent(self, aid):
    # Makes sure that no agent with the standard ID remains
    self.client.delete_agent(aid)

  def clean_up_agents(self, aids):
    # Makes sure that no agent with the standard ID remains
    for aid in aids:
      self.clean_up_agent(aid)

  def test_get_one_decision_tree_with_correct_input(self):
    payload = [{"id": self.agent_id1, "timestamp": valid_data.VALID_TIMESTAMP}]

    decision_trees = self.client.get_bulk_decision_trees(payload)

    self.assertIsInstance(decision_trees, list)
    self.assertIsInstance(decision_trees[0], dict)
    self.assertIsInstance(decision_trees[0].get("tree"), dict)
    self.assertNotEqual(decision_trees[0].get("tree").get("_version"), None)
    self.assertNotEqual(decision_trees[0].get("tree").get("configuration"), None)
    self.assertNotEqual(decision_trees[0].get("tree").get("trees"), None)

    self.addCleanup(self.clean_up_agents,
                    [self.agent_id1, self.agent_id2])

  def test_get_all_decision_trees_with_correct_input(self):
    payload = [{"id": self.agent_id1, "timestamp": valid_data.VALID_TIMESTAMP},
               {"id": self.agent_id2, "timestamp": valid_data.VALID_TIMESTAMP}]

    decision_trees = self.client.get_bulk_decision_trees(payload)

    self.assertIsInstance(decision_trees, list)
    self.assertIsInstance(decision_trees[0], dict)
    self.assertEqual(decision_trees[0].get("id"),self.agent_id1)
    self.assertIsInstance(decision_trees[0].get("tree"), dict)
    self.assertNotEqual(decision_trees[0].get("tree").get("_version"), None)
    self.assertNotEqual(decision_trees[0].get("tree").get("configuration"), None)
    self.assertNotEqual(decision_trees[0].get("tree").get("trees"), None)
    self.assertIsInstance(decision_trees[1], dict)
    self.assertEqual(decision_trees[1].get("id"),self.agent_id2)
    self.assertIsInstance(decision_trees[1].get("tree"), dict)
    self.assertNotEqual(decision_trees[1].get("tree").get("_version"), None)
    self.assertNotEqual(decision_trees[1].get("tree").get("configuration"), None)
    self.assertNotEqual(decision_trees[1].get("tree").get("trees"), None)

    self.addCleanup(self.clean_up_agents,
                    [self.agent_id1, self.agent_id2])

  def test_get_bulk_decision_trees_specific_version(self):
    payload = [{"id": self.agent_id1, "timestamp": valid_data.VALID_TIMESTAMP},
               {"id": self.agent_id2, "timestamp": valid_data.VALID_TIMESTAMP}]
    version = 1
    decision_trees = self.client.get_bulk_decision_trees(payload, version)

    self.assertNotEqual(decision_trees[0].get("tree").get("_version"), None)
    tree_version = semver.parse(decision_trees[0].get("tree").get("_version"))
    self.assertEqual(tree_version["major"], version)
    self.assertNotEqual(decision_trees[1].get("tree").get("_version"), None)
    tree_version = semver.parse(decision_trees[1].get("tree").get("_version"))
    self.assertEqual(tree_version["major"], version)

    self.addCleanup(self.clean_up_agents,
                    [self.agent_id1, self.agent_id2])

  def test_get_bulk_decision_trees_without_timestamp(self):
    payload = [{"id": self.agent_id1},
               {"id": self.agent_id2}]
    decision_trees = self.client.get_bulk_decision_trees(payload)
    ground_truth_decision_tree1 = self.client.get_decision_tree(self.agent_id1, 1458741262)
    ground_truth_decision_tree2 = self.client.get_decision_tree(self.agent_id2, 1458741262)

    self.assertEqual(decision_trees[0].get("tree"), ground_truth_decision_tree1)
    self.assertEqual(decision_trees[1].get("tree"), ground_truth_decision_tree2)

    self.addCleanup(self.clean_up_agents,
                    [self.agent_id1, self.agent_id2])


class TestGetDecisionTreeFail(unittest.TestCase):
  """Checks that the client succeeds when getting
  an/multiple decision tree(s) with OK input"""

  @classmethod
  def setUpClass(cls):
    cls.client = Client(settings.CRAFT_CFG)
    cls.agent_id1 = valid_data.VALID_ID  + "_" + settings.RUN_ID
    cls.agent_id2 = valid_data.VALID_ID_TWO  + "_" + settings.RUN_ID
    cls.VALID_L_OPERATIONS = [
      [
        {
          "timestamp": batch_offset * VALID_L_BATCH_DURATION + operation_offset,
          "context": {
            "e1": random.choice(VALID_L_ENUM_VALUES),
            "e2": random.choice(VALID_L_ENUM_VALUES),
            "e3": random.choice(VALID_L_ENUM_VALUES),
            "e4": random.choice(VALID_L_ENUM_VALUES),
            "c1": random.uniform(-12, 12),
            "c2": random.uniform(-12, 12),
            "c3": random.uniform(-12, 12),
            "c4": random.uniform(-12, 12),
            "tz": "CET"
          }
        }
        for operation_offset in range(0, VALID_L_BATCH_DURATION, 1000)
      ]
    for batch_offset in range(0, 60)
    ]

  def setUp(self):
    # Makes sure that no agent with the same ID already exists
    self.client.delete_agent(self.agent_id1)
    self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id1)
    self.client.add_operations(self.agent_id1, valid_data.VALID_OPERATIONS_SET)

    self.client.delete_agent(self.agent_id2)
    self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id2)
    self.client.add_operations(self.agent_id2, valid_data.VALID_OPERATIONS_SET)

  def clean_up_agent(self, aid):
    # Makes sure that no agent with the standard ID remains
    self.client.delete_agent(aid)

  def clean_up_agents(self, aids):
    # Makes sure that no agent with the standard ID remains
    for aid in aids:
      self.clean_up_agent(aid)

  def test_get_all_decision_trees_with_invalid_id(self):
    """get_decision_tree should fail when given a non-string/empty string ID

    It should raise an error upon request for retrieval of an agent's
    decision tree with an ID that is not of type string, since agent IDs
    should always be strings.
    """
    for empty_id in invalid_data.UNDEFINED_KEY:
      payload = [{"id": invalid_data.UNDEFINED_KEY[empty_id], "timestamp": valid_data.VALID_TIMESTAMP},
                 {"id": invalid_data.UNDEFINED_KEY[empty_id], "timestamp": valid_data.VALID_TIMESTAMP}]
      self.assertRaises(
        craft_err.CraftAiBadRequestError,
        self.client.get_decision_tree,
        payload
      )
      self.addCleanup(self.clean_up_agents,
                      [self.agent_id1, self.agent_id2])
  
  def test_get_all_decision_trees_with_unknown_id(self):
    """get_decision_tree should fail when given a non-string/empty string ID

    It should raise an error upon request for retrieval of an agent's
    decision tree with an ID that is not of type string, since agent IDs
    should always be strings.
    """
    payload = [{"id": invalid_data.UNKNOWN_ID, "timestamp": valid_data.VALID_TIMESTAMP},
               {"id": invalid_data.UNKNOWN_ID_TWO, "timestamp": valid_data.VALID_TIMESTAMP}]
    self.assertRaises(
      craft_err.CraftAiBadRequestError,
      self.client.get_decision_tree,
      payload
    )
    self.addCleanup(self.clean_up_agents,
                    [self.agent_id1, self.agent_id2])

#timestamp