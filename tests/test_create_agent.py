import unittest

from craftai import client as craft_client
from craftai import errors as craft_err

valid_id = "rainbow unicorn"
valid_context = {
    "presence": {
        "type": "enum"
    },
    "lightIntensity": {
        "type": "continuous"
    },
    "lightbulbColor": {
        "type": "enum"
    }
}
valid_output = ["lightbulbColor"]
valid_tq = 100
valid_model = {
    "model": {
        "context": valid_context,
        "output": valid_output,
        "time_quantum": valid_tq
    }
}

invalid_ids = (("bad_id_type", 42),
               ("empty_id", ""),
               ("undefined_id", None))

invalid_contexts = (("no_context", None),
                    ("empty_context", {}),
                    ("invalid_context_type", {
                        "presence": {
                            "type": "chair"
                        },
                        "lightIntensity": {
                            "type": "continuous"
                        },
                        "lightbulbColor": {
                            "type": "enum"
                        }
                    }),
                    ("invalid_context_missing_type_key", {
                        "context": {
                            "presence": {
                                "typo": "enum"
                            },
                            "lightIntensity": {
                                "type": "continuous"
                            },
                            "lightbulbColor": {
                                "type": "enum"
                            }
                        },
                        "output": ["lightbulbColor"],
                        "time_quantum": 100
                    }))

invalid_outputs = (("no_output", None),
                   ("output_not_in_the_model", ["beerBrand"]))

unspecified_models = (None,
                      "",
                      {})

invalid_time_quanta = (("negative_tq", -42),
                       ("null_tq", 0),
                       ("high_tq", 4294967296),
                       ("float_tq", 3.141592))


class TestCreateAgent(unittest.TestSuite):
    """docstring for TestCreateAgent"""
    def __init__(self, arg):
        super(TestCreateAgent, self).__init__()
        self.arg = arg


class TestCreateAgentSuccess(unittest.TestCase):
    """Checks that the client succeeds when creating an agent with OK input"""

    def test_create_agent_with_generated_agent_id(self):
        """create_agent should succeed when given an empty `id` field

        It should give a proper JSON response with `id` and
        `model` fields being strings.
        """
        resp = craft_client.create_agent(valid_model)
        self.assertTrue(isinstance(resp.id, basestring))

    def test_create_agent_given_agent_id(self):
        """create_agent should succeed when given a string ID

        It should give a proper JSON response with `id` and
        `model` fields being strings and `id` being the same as the one
        given as a parameter.
        """
        resp = craft_client.create_agent(valid_model, valid_id)
        self.assertEqual(resp.id, valid_id)


class TestCreateAgentFailure(unittest.TestCase):
    """Checks that the client fails when creating an agent with bad input"""

    def test_create_agent_with_invalid_given_agent_id(self):
        """create_agent should fail when given a non-string ID

        It should raise an error upon request for creation of
        an agent with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        for inv_id in invalid_ids:
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                craft_client.create_agent,
                valid_model,
                inv_id)

    def test_create_agent_with_existing_agent_id(self):
        """create_agent should fail when given an ID that already exists

        It should raise an error upon request for creation of
        an agent with an ID that already exists, since agent IDs
        should always be unique.
        """
        # Calling create_agent a first time
        craft_client.create_agent(valid_model, valid_id)
        # Asserting that an error is risen the second time
        self.assertRaises(
            craft_err.CraftAIBadRequestError,
            craft_client.create_agent,
            valid_model,
            valid_id)

    def test_create_agent_with_invalid_context(self):
        """create_agent should fail when given an invalid or no context

        It should raise an error upon request for creation of
        an agent with no context or a context that is invalid.
        """
        for inv_context in invalid_contexts:
            model = {
                "model": {
                    "context": inv_context,
                    "output": ["lightbulbColor"],
                    "time_quantum": 100
                }
            }
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                craft_client.create_agent,
                model,
                valid_id)

    def test_create_agent_with_invalid_output(self):
        """create_agent should fail when given no or an invalid output

        It should raise an error upon request for creation of an agent
        with no specified output or one that doesn't exist in the
        model, since it is a mandatory key in the model.
        """
        for inv_output in invalid_outputs:
            model = {
                "model": {
                    "context": valid_context,
                    "output": inv_output,
                    "time_quantum": 100
                }
            }
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                craft_client.create_agent,
                model,
                valid_id)

    def test_create_agent_with_undefined_model(self):
        """create_agent should fail when given no model key in the request body

        It should raise an error upon request for creation of an agent with
        no model key in the request body, since it is a mandatory field to
        create an agent.
        """
        for empty_model in unspecified_models:
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                craft_client.create_agent,
                empty_model,
                valid_id)

    def test_create_agent_with_invalid_time_quantum(self):
        """create_agent should fail when given an invalid time quantum

        It should raise an error upon request for creation of an agent with
        an incorrect time quantum in the model, since it is essential to
        perform any action with craft ai.
        """
        for inv_tq in invalid_time_quanta:
            model = {
                "model": {
                    "context": valid_context,
                    "output": valid_output,
                    "time_quantum": inv_tq
                }
            }
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                craft_client.create_agent,
                model,
                valid_id)
