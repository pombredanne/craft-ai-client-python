

class CraftAIClient():
    """docstring for CraftAIClient"""
    def __init__(self, cfg):
        super(CraftAIClient, self).__init__()
        self.config = cfg

    def config(self, cfg):
        self.cfg = cfg

    def create_agent(self, agent_id, model):
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
