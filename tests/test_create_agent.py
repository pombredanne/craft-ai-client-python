import unittest
import six

from . import settings
from .data import valid_data
from .data import invalid_data
from craftai.client import CraftAIClient
from craftai import errors as craft_err


class TestCreateAgentSuccess(unittest.TestCase):
    """Checks that the client succeeds when creating an agent with OK input"""

    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        # Makes sure that no agent with the same ID already exists
        self.client.delete_agent(valid_data.VALID_ID)

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def test_create_agent_with_generated_agent_id(self):
        """create_agent should succeed when given an empty `id` field

        It should give a proper JSON response with `id` and
        `model` fields being strings.
        """
        resp = self.client.create_agent(valid_data.VALID_MODEL)
        self.assertIsInstance(resp.get("id"), six.string_types)
        self.addCleanup(self.clean_up_agent, resp.get("id"))

    def test_create_agent_given_agent_id(self):
        """create_agent should succeed when given a string ID

        It should give a proper JSON response with `id` and
        `model` fields being strings and `id` being the same as the one
        given as a parameter.
        """
        resp = self.client.create_agent(
            valid_data.VALID_MODEL,
            valid_data.VALID_ID)
        self.assertEqual(resp.get("id"), valid_data.VALID_ID)
        self.addCleanup(self.clean_up_agent, valid_data.VALID_ID)


class TestCreateAgentFailure(unittest.TestCase):
    """Checks that the client fails when creating an agent with bad input"""

    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        # Makes sure that no agent with the same ID already exists
        self.client.delete_agent(valid_data.VALID_ID)

    def test_create_agent_with_invalid_given_agent_id(self):
        """create_agent should fail when given a non-string/empty string ID

        It should raise an error upon request for creation of
        an agent with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        for inv_id in invalid_data.INVALID_IDS:
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.create_agent,
                valid_data.VALID_MODEL,
                invalid_data.INVALID_IDS[inv_id])

    def test_create_agent_with_existing_agent_id(self):
        """create_agent should fail when given an ID that already exists

        It should raise an error upon request for creation of
        an agent with an ID that already exists, since agent IDs
        should always be unique.
        """
        # Calling create_agent a first time
        self.client.create_agent(valid_data.VALID_MODEL, valid_data.VALID_ID)
        # Asserting that an error is risen the second time
        self.assertRaises(
            craft_err.CraftAIBadRequestError,
            self.client.create_agent,
            valid_data.VALID_MODEL,
            valid_data.VALID_ID)

    def test_create_agent_with_invalid_context(self):
        """create_agent should fail when given an invalid or no context

        It should raise an error upon request for creation of
        an agent with no context or a context that is invalid.
        """
        for inv_context in invalid_data.INVALID_CONTEXTS:
            model = {
                "context": invalid_data.INVALID_CONTEXTS[inv_context],
                "output": ["lightbulbColor"],
                "time_quantum": 100
            }
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.create_agent,
                model,
                valid_data.VALID_ID)

    def test_create_agent_with_invalid_output(self):
        """create_agent should fail when given no or an invalid output

        It should raise an error upon request for creation of an agent
        with no specified output or one that doesn't exist in the
        model, since it is a mandatory key in the model.
        """
        for inv_output in invalid_data.INVALID_OUTPUTS:
            model = {
                "context": valid_data.VALID_CONTEXT,
                "output": invalid_data.INVALID_OUTPUTS[inv_output],
                "time_quantum": 100
            }
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.create_agent,
                model,
                valid_data.VALID_ID)

    def test_create_agent_with_undefined_model(self):
        """create_agent should fail when given no model key in the request body

        It should raise an error upon request for creation of an agent with
        no model key in the request body, since it is a mandatory field to
        create an agent.
        """

        # Testing all non dict model cases
        for empty_model in invalid_data.UNDEFINED_KEY:
            if not isinstance(invalid_data.UNDEFINED_KEY[empty_model], dict):
                self.assertRaises(
                    craft_err.CraftAIBadRequestError,
                    self.client.create_agent,
                    invalid_data.UNDEFINED_KEY[empty_model],
                    valid_data.VALID_ID)

    def test_create_agent_with_unknown_model(self):
        """create_agent should fail when given an unknown model

        It should raise an error upon request for creation of an agent with
        no valid model in the request body, since it is a mandatory field to
        create an agent.
        """
        # Testing all dict model cases
        for empty_model in invalid_data.UNDEFINED_KEY:
            if isinstance(invalid_data.UNDEFINED_KEY[empty_model], dict):
                self.assertRaises(
                    craft_err.CraftAINotFoundError,
                    self.client.create_agent,
                    invalid_data.UNDEFINED_KEY[empty_model],
                    valid_data.VALID_ID)

    def test_create_agent_with_invalid_time_quantum(self):
        """create_agent should fail when given an invalid time quantum

        It should raise an error upon request for creation of an agent with
        an incorrect time quantum in the model, since it is essential to
        perform any action with craft ai.
        """
        for inv_tq in invalid_data.INVALID_TIME_QUANTA:
            print(invalid_data.INVALID_TIME_QUANTA[inv_tq])
            model = {
                "context": valid_data.VALID_CONTEXT,
                "output": valid_data.VALID_OUTPUT,
                "time_quantum": invalid_data.INVALID_TIME_QUANTA[inv_tq]
            }
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.create_agent,
                model,
                valid_data.VALID_ID)
