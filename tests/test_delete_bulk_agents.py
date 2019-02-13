import unittest
import six

from nose.tools import nottest
from craftai import Client, errors as craft_err

from . import settings
from .data import valid_data
from .data import invalid_data

class TestDeleteBulkAgentsSuccess(unittest.TestCase):
  """Checks that the client succeeds when deleting
  an/multiple agent(s) with OK input"""

  @classmethod
  def setUpClass(cls):
    cls.client = Client(settings.CRAFT_CFG)
    cls.agent_id1 = valid_data.VALID_ID  + "_" + settings.RUN_ID
    cls.agent_id2 = valid_data.VALID_ID  + "_" + settings.RUN_ID

  def setUp(self):
    # Creating an agent may raise an error if one with the same ID
    # already exists. Although it shouldn' matter for the deletion test,
    # it is necessary to catch this kind of errors.
    try:
      self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id1)
      self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id2)
    except craft_err.CraftAiBadRequestError as e:
      if "one already exists" not in e.message:
        raise e

  def test_delete_one_agent_with_valid_id(self):
    """delete_bulk_agents should succeed when given an valid `id`.

    It should give a proper JSON response with a list containing a dict
    with `id` being the same as the one given as a parameter.
    """
    payload = [{"id": self.agent_id1}]
    resp = self.client.delete_bulk_agents(payload)

    self.assertEqual(resp[0].get("id"), self.agent_id1)

  def test_delete_multiple_agents_with_valid_id(self):
    """delete_bulk_agents should succeed when given multiple valid `id`s.

    It should give a proper JSON response with a list containing two dicts
    with the `id`s being the same as the ones given as parameters.
    """
    payload = [{"id": self.agent_id1}, {"id": self.agent_id2}]
    resp = self.client.delete_bulk_agents(payload)

    self.assertEqual(resp[0].get("id"), self.agent_id1)
    self.assertEqual(resp[1].get("id"), self.agent_id2)


class TestDeleteBulkAgentsFail(unittest.TestCase):
  """Checks that the client succeeds when deleting
  an/multiple agent(s) with invalid input"""

  @classmethod
  def setUpClass(cls):
    cls.client = Client(settings.CRAFT_CFG)
    cls.agent_id1 = valid_data.VALID_ID  + "_" + settings.RUN_ID
    cls.agent_id2 = valid_data.VALID_ID  + "_" + settings.RUN_ID

  def setUp(self):
    # Creating an agent may raise an error if one with the same ID
    # already exists. Although it shouldn' matter for the deletion test,
    # it is necessary to catch this kind of errors.
    try:
      self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id1)
      self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id2)
    except craft_err.CraftAiBadRequestError as e:
      if "one already exists" not in e.message:
        raise e

  def test_delete_multiple_agents_with_invalid_id(self):
    """delete_bulk_agents should fail when given multiple
    invalid `id`s.

    It should raise an error upon request for the deletion of a bulk of 
    agents with invalid IDs.
    """
    payload = [{"id": "toto/tutu"}, {"id": "toto@tata"}]
    self.assertRaises(
      craft_err.CraftAiBadRequestError,
      self.client.delete_bulk_agents,
      payload
    )

class TestDeleteBulkAgentsSomeFailure(unittest.TestCase):
  """Checks that the client succeed when deleting
  an/multiple agent(s) with bad input and an/multiple agent(s)
  with valid input"""

  @classmethod
  def setUpClass(cls):
    cls.client = Client(settings.CRAFT_CFG)
    cls.agent_id1 = valid_data.VALID_ID  + "_" + settings.RUN_ID
    cls.agent_id2 = valid_data.VALID_ID  + "_" + settings.RUN_ID

  def setUp(self):
    # Creating an agent may raise an error if one with the same ID
    # already exists. Although it shouldn' matter for the deletion test,
    # it is necessary to catch this kind of errors.
    try:
      self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id1)
      self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id2)
    except craft_err.CraftAiBadRequestError as e:
      if "one already exists" not in e.message:
        raise e

  def test_delete_some_agents_with_invalid_id(self):
    """delete_bulk_agents should succeed when given some
    invalid `id`s and some valid.

    It should give a proper JSON response with a list containing two dicts.
    The first one should have 'id' being the same as the one given as a parameter,
    'error' field being a CraftAiBadRequestError.
    The second one should have `id` being the same as the one given as a parameter.    
    """
    payload = [{"id": "toto/tutu"}, {"id": self.agent_id2}]
    resp = self.client.delete_bulk_agents(payload)

    self.assertEqual(resp[0].get("id"), "toto/tutu")
    self.assertTrue("error" in resp[0])
    self.assertIsInstance(resp[0].get("error"), craft_err.CraftAiBadRequestError)
    self.assertEqual(resp[1].get("id"), self.agent_id2)
    self.assertFalse("error" in resp[1])
