import unittest

from . import settings
from tests.data import valid_data
from tests.data import invalid_data

from craftai.client import CraftAIClient
from craftai import errors as craft_err


class TestGetOperationsListSuccess(unittest.TestCase):
    """Checks that the client succeeds when retrieving an agent's operations
    with OK input.
    """
    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        self.client.delete_agent(valid_data.VALID_ID)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, valid_data.VALID_ID)
        self.client.add_operations(
            valid_data.VALID_ID,
            valid_data.VALID_OPERATIONS_SET)

    def tearDown(self):
        self.client.delete_agent(valid_data.VALID_ID)

    def test_get_operations_list_with_correct_data(self):
        """get_operations_list should succeed when given a correct agent ID

        It should give a proper JSON response as a list of dicts.
        """
        ops = self.client.get_operations_list(valid_data.VALID_ID)
        self.assertIsInstance(ops, list)


class TestGetOperationsListFailure(unittest.TestCase):
    """Checks that the client fails properly when getting an agent with bad
    input"""
    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        self.client.delete_agent(valid_data.VALID_ID)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, valid_data.VALID_ID)
        self.client.add_operations(
            valid_data.VALID_ID,
            valid_data.VALID_OPERATIONS_SET)

    def tearDown(self):
        self.client.delete_agent(valid_data.VALID_ID)

    def test_get_operations_list_with_invalid_id(self):
        """get_operations_list should fail when given a non-string/empty ID

        It should raise an error upon request for retrieval of
        an agent's context operations for an agent that is not of type string,
        since agent IDs should always be strings.
        """
        for empty_id in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_err.CraftAiBadRequestError,
                self.client.get_operations_list,
                invalid_data.UNDEFINED_KEY[empty_id])

    # def test_get_operations_list_with_unknown_id(self):
    #     """get_operations_list should fail when given an unknown agent ID

    #     It should raise an error upon request for the retrieval of an agent
    #     that doesn't exist.
    #     """
    #     self.assertRaises(
    #         craft_err.CraftAiNotFoundError,
    #         self.client.get_operations_list,
    #         invalid_data.UNKNOWN_ID)
