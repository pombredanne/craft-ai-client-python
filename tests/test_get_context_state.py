import unittest

from . import settings
from tests.data import valid_data
from tests.data import invalid_data

from craftai.client import CraftAIClient
from craftai import errors as craft_err


class TestGetContextStateSuccess(unittest.TestCase):
    """Checks that the client succeeds when retrieving an agent's current state
    with OK input.
    """
    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        self.client.delete_agent(valid_data.VALID_ID)
        self.client.create_agent(valid_data.VALID_MODEL, valid_data.VALID_ID)
        self.client.add_operations(
            valid_data.VALID_ID,
            valid_data.VALID_OPERATIONS_SET)

    def tearDown(self):
        self.client.delete_agent(valid_data.VALID_ID)

    def test_get_context_state_with_correct_input(self):
        """get_context_state should succeed when given proper ID and timestamp.

        It should give a proper JSON response with `timestamp` field being an
        integer and equal to the requested one, and a `diff` field containing
        a dict.
        """
        context_state = self.client.get_context_state(
            valid_data.VALID_ID,
            valid_data.VALID_TIMESTAMP)
        self.assertIsInstance(context_state, dict)
        context_state_keys = context_state.keys()
        self.assertTrue("timestamp" in context_state_keys)
        self.assertIsInstance(context_state["timestamp"], int)
        self.assertEqual(
            context_state["timestamp"],
            valid_data.VALID_TIMESTAMP)


class TestGetContextStateFailure(unittest.TestCase):
    """Checks that the client fails properly when getting an agent's context
    with bad input"""
    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        self.client.delete_agent(valid_data.VALID_ID)
        self.client.create_agent(valid_data.VALID_MODEL, valid_data.VALID_ID)
        self.client.add_operations(
            valid_data.VALID_ID,
            valid_data.VALID_OPERATIONS_SET)

    def tearDown(self):
        self.client.delete_agent(valid_data.VALID_ID)

    def test_get_context_state_with_invalid_id(self):
        """get_context_state should fail when given a non-string/empty string ID

        It should raise an error upon request for retrieval of
        an agent with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        for empty_id in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.get_context_state,
                invalid_data.UNDEFINED_KEY[empty_id],
                valid_data.VALID_TIMESTAMP)

    def test_get_context_state_with_unknown_id(self):
        """get_context_state should fail when given an unknown agent ID

        It should raise an error upon request for the retrieval of an agent
        that doesn't exist.
        """
        self.assertRaises(
            craft_err.CraftAINotFoundError,
            self.client.get_context_state,
            invalid_data.UNKNOWN_ID,
            valid_data.VALID_TIMESTAMP)

    def test_get_context_state_with_invalid_timestamp(self):
        for inv_ts in invalid_data.INVALID_TIMESTAMPS:
            print(inv_ts)
            if not (inv_ts is None):
                self.assertRaises(
                    craft_err.CraftAIBadRequestError,
                    self.client.get_context_state,
                    valid_data.VALID_ID,
                    invalid_data.INVALID_TIMESTAMPS[inv_ts])
