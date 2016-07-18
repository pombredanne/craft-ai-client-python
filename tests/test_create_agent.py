import unittest


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
        pass

    def test_create_agent_given_agent_id(self):
        """create_agent should succeed when given a string ID

        It should give a proper JSON response with `id` and
        `model` fields being strings and `id` being the same as the one
        given as a parameter.
        """
        pass


class TestCreateAgentFailure(unittest.TestCase):
    """Checks that the client fails when creating an agent with bad input"""

    def test_create_agent_with_invalid_given_agent_id(self):
        """create_agent should fail when given a non-string ID

        It should raise an error upon request for creation of
        an agent with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        pass

    def test_create_agent_with_existing_agent_id(self):
        """create_agent should fail when given a ID that already exists

        It should raise an error upon request for creation of
        an agent with an ID that already exists, since agent IDs
        should always be unique.
        """
        pass

    def test_create_agent_with_invalid_context(self):
        """create_agent should fail when given an invalid context

        It should raise an error upon request for creation of
        an agent with no context or a context that is invalid.
        """
        pass

    def test_create_agent_with_invalid_output(self):
        """create_agent should fail when given no or an invalid output

        It should raise an error upon request for creation of an agent
        with no specified output or one that doesn't exist in the
        model, since it is a mandatory key in the model.
        """
        pass

    def test_create_agent_with_undefined_model(self):
        """create_agent should fail when given no model key in the request body

        It should raise an error upon request for creation of an agent with
        no model key in the request body, since it is a mandatory field to
        create an agent.
        """
        pass

    def test_create_agent_with_invalid_time_quantum(self):
        """create_agent should fail when given an invalid time quantum

        It should raise an error upon request for creation of an agent with
        an incorrect time quantum in the model, since it is essential to
        perform any action with craft ai.
        """
        pass
