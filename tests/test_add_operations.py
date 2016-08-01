import unittest
import six

from . import settings
from tests.data import valid_data
from tests.data import invalid_data

from craftai.client import CraftAIClient
from craftai import errors as craft_err


class TestAddOperationsSuccess(unittest.TestCase):
    """Checks that the client succeeds when getting an agent with OK input"""

    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        self.client.delete_agent(valid_data.VALID_ID)
        self.client.create_agent(valid_data.VALID_MODEL, valid_data.VALID_ID)

    def tearDown(self):
        self.client.delete_agent(valid_data.VALID_ID)

    def test_add_operations_with_correct_input(self):
        """add_operations should succeed when given correct input data

        It should give a proper JSON response with a `message` fields being a
        string.
        """
        resp = self.client.add_operations(
            valid_data.VALID_ID,
            valid_data.VALID_OPERATIONS_SET)

        self.assertIsInstance(resp, dict)
        resp_keys = resp.keys()
        self.assertTrue("message" in resp_keys)


class TestAddOperationsFailure(unittest.TestCase):
    """Checks that the client fails properly when getting an agent with bad
    input"""

    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        self.client.delete_agent(valid_data.VALID_ID)
        self.client.create_agent(valid_data.VALID_MODEL, valid_data.VALID_ID)

    def tearDown(self):
        self.client.delete_agent(valid_data.VALID_ID)

    def test_add_operations_with_invalid_agent_id(self):
        """add_operations should fail when given a non-string/empty string ID

        It should raise an error upon request for operations posting
        for an agent with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        for empty_id in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.add_operations,
                invalid_data.UNDEFINED_KEY[empty_id],
                valid_data.VALID_OPERATIONS_SET)

    def test_add_operations_with_unknown_id(self):
        """add_operations should fail when given an unknown agent ID

        It should raise an error upon request for operations posting to an
        agent's model, for which the agent doesn't exist.
        """
        self.assertRaises(
            craft_err.CraftAINotFoundError,
            self.client.add_operations,
            invalid_data.UNKNOWN_ID,
            valid_data.VALID_OPERATIONS_SET)

    def test_add_operations_with_empty_operations_set(self):
        """add_operations should fail when given an empty set of operations

        It should raise an error upon request for posting an empty set of
        operations to an agent's model.
        """
        for ops_set in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.add_operations,
                valid_data.VALID_ID,
                invalid_data.UNDEFINED_KEY[ops_set])

    def test_add_operations_with_invalid_operation_set(self):
        for ops_set in invalid_data.INVALID_OPS_SET:
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.add_operations,
                valid_data.VALID_ID,
                invalid_data.INVALID_OPS_SET[ops_set])
