import unittest
import json
import os

import craftai

from . import settings
from .data import valid_data, invalid_data

HERE = os.path.abspath(os.path.dirname(__file__))

LARGE_VALID_OPERATIONS_SET = []
with open(os.path.join(HERE, "./data/large_operation_list.json")) as large_operation_list_file:
  LARGE_VALID_OPERATIONS_SET = json.load(large_operation_list_file)


class TestGetOperationsListSuccess(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.client = craftai.Client(settings.CRAFT_CFG)
    cls.agent_id = valid_data.VALID_ID  + "_" + settings.RUN_ID

  def setUp(self):
    self.client.delete_agent(self.agent_id)
    self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)

    self.client.add_operations(
      self.agent_id,
      LARGE_VALID_OPERATIONS_SET)

  def tearDown(self):
    self.client.delete_agent(self.agent_id)

  def test_get_operations_list_with_correct_data(self):
    ops = self.client.get_operations_list(self.agent_id)
    self.assertIsInstance(ops, list)
    self.assertEqual(ops, LARGE_VALID_OPERATIONS_SET)


class TestGetOperationsListFailure(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.client = craftai.Client(settings.CRAFT_CFG)
    cls.agent_id = valid_data.VALID_ID  + "_" + settings.RUN_ID

  def setUp(self):
    self.client.delete_agent(self.agent_id)
    self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)
    self.client.add_operations(
      self.agent_id,
      valid_data.VALID_OPERATIONS_SET)

  def tearDown(self):
    self.client.delete_agent(self.agent_id)

  def test_get_operations_list_with_invalid_id(self):
    for empty_id in invalid_data.UNDEFINED_KEY:
      self.assertRaises(
        craftai.errors.CraftAiBadRequestError,
        self.client.get_operations_list,
        invalid_data.UNDEFINED_KEY[empty_id])
