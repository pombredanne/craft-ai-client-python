import requests
import json
import six

from craftai.errors import *


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
        headers = {}
        headers["Authorization"] = "Bearer " + self.cfg.get("token")
        headers["Content-Type"] = "application/json; charset=utf-8"
        headers["Accept"] = "application/json"
        url = "".join((
            self.cfg.get("url"),
            "api/",
            self.cfg.get("owner"),
            "/agents"))

        payload = {
            "id": agent_id,
            "model": model
        }

        # Checking that the sent model is valid for a JSON serialization
        try:
            json.dumps(payload)
        except TypeError as e:
            raise CraftAIBadRequestError(
                "".join(("Invalid model or agent id given. ",
                        e.__str__())))

        r = requests.post(url, headers=headers, json=payload)

        if r.status_code == requests.codes.not_found:
            raise CraftAINotFoundError(r.text)
        if r.status_code == requests.codes.bad_request:
            raise CraftAIBadRequestError(r.text)

        try:
            agent = r.json()
        except json.JSONDecodeError:
            raise CraftAIUnknownError(r.text)

        return agent

    def get_agent(self, agent_id):
        pass

    def delete_agent(self, agent_id):
        if not (agent_id and isinstance(agent_id, six.string_types)):
            raise CraftAIBadRequestError("agent_id has to be a string")

        headers = {}
        headers["Authorization"] = "Bearer " + self.cfg.get("token")
        headers["Accept"] = "application/json"
        url = "".join((
            self.cfg.get("url"),
            "api/",
            self.cfg.get("owner"),
            "/agents/",
            agent_id)
        )

        r = requests.delete(url, headers=headers)
        # print(r.body)

        if r.status_code == requests.codes.bad_request:
            raise CraftAIBadRequestError(r.text)

        try:
            resp = r.json()
        except json.JSONDecodeError:
            raise CraftAIUnknownError(r.text)

        return resp

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
