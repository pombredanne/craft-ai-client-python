import six

from craftai.errors import CraftAICredentialsError
from craftai.errors import CraftAIBadRequestError


class CraftAIClient():
    """docstring for CraftAIClient"""
    def __init__(self, cfg):
        super(CraftAIClient, self).__init__()
        try:
            self.set_config(cfg)
        except (CraftAICredentialsError, CraftAIBadRequestError) as e:
            raise e

    def set_config(self, cfg):
        if (not isinstance(cfg.get("token"), six.string_types)):
            raise CraftAICredentialsError("""Unable to create client with no"""
                                          """ or invalid token provided.""")
        if (not isinstance(cfg.get("owner"), six.string_types)):
            raise CraftAICredentialsError("""Unable to create client with no"""
                                          """ or invalid owner provided.""")
        if (not isinstance(cfg.get("url"), six.string_types)):
            raise CraftAIBadRequestError("""Unable to create client with no"""
                                         """ or invalid url provided.""")
        if (cfg.get("url")[-1] != '/'):
            raise CraftAIBadRequestError("""Unable to create client with"""
                                         """ invalid url provided. The url"""
                                         """ should terminate with a slash.""")
        self.cfg = cfg

    def create_agent(self, model, agent_id=""):
        pass

    def get_agent(self, agent_id):
        pass

    def delete_agent(self, agent_id):
        pass

    def add_operations(self, agent_id, operations):
        pass

    def get_operations_list(self, agent_id):
        pass

    def get_context_state(self, agent_id, timestamp):
        pass

    def get_decision_tree(self, agent_id, timestamp):
        pass

    def get_decision_from_context(self, agent_id, timestamp, decision_context):
        pass
