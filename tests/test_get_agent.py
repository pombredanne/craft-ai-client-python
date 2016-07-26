import unittest

from . import settings
from .data import valid_data
from .data import invalid_data
from craftai.client import CraftAIClient
from craftai import errors as craft_err


class TestGetAgentSuccess(unittest.TestCase):
    """Checks that the client succeeds when getting an agent with OK input"""
    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        self.client.delete_agent(valid_data.VALID_ID)
        self.client.create_agent(valid_data.VALID_MODEL, valid_data.VALID_ID)

    def tearDown(self):
        self.client.delete_agent(valid_data.VALID_ID)

    def test_get_agent_with_correct_id(self):
        """get_agent should succeed when given a correct agent ID

        It should give a proper JSON response with `model`, `firstTimestamp`
        and `lastTimestamp` fields being strings.
        """
        agent = self.client.get_agent(valid_data.VALID_ID)
        self.assertIsInstance(agent, dict)
        self.assertDictContainsSubset("model", agent)
        self.assertDictContainsSubset("firstTimestamp", agent)
        self.assertDictContainsSubset("lastTimestamp", agent)


class TestGetAgentFailure(unittest.TestCase):
    """Checks that the client fails properly when getting an agent with bad
    input"""
    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        # Makes sure that no agent exists with the test id
        # (especially for test_get_agent_with_unknown_id)
        self.client.delete_agent(valid_data.VALID_ID)

    def test_get_agent_with_invalid_id(self):
        """create_agent should fail when given a non-string/empty string ID

        It should raise an error upon request for retrieval of
        an agent with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        for empty_id in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.get_agent,
                empty_id)

    def test_get_agent_with_unknown_id(self):
        """get_agent should fail when given no model key in the request body

        It should raise an error upon request for the retrieval of an agent
        that doesn't exist.
        """
        self.assertRaises(
            craft_err.CraftAINotFoundError,
            self.client.get_agent,
            valid_data.VALID_ID)
