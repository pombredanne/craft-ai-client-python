import requests
import json
import six

from craftai import helpers

from craftai.errors import *


class CraftAIClient(object):
    """docstring for CraftAIClient"""
    def __init__(self, cfg):
        self._base_url = ""
        self._headers = {}

        try:
            self.config = cfg
        except (CraftAICredentialsError, CraftAIBadRequestError) as e:
            raise e

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, cfg):
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
        self._config = cfg

        self._base_url = "".join((
            self.config.get("url"),
            "api/",
            self.config.get("owner")))

        # Headers have to be reset here to avoid multiple definitions
        # of the 'Authorization' header if config is modified
        self._headers = {}
        self._headers["Authorization"] = "Bearer " + self.config.get("token")

    def create_agent(self, model, agent_id=""):
        # Building final headers
        ct_header = {"Content-Type": "application/json; charset=utf-8"}
        headers = helpers.join_headers(self._headers, ct_header)

        # Building payload and checking that it is valid for a JSON
        # serialization
        payload = {
            "id": agent_id,
            "model": model
        }
        try:
            json_pl = json.dumps(payload)
        except TypeError as e:
            raise CraftAIBadRequestError(
                "".join(("Invalid model or agent id given. ",
                        e.__str__())))

        req_url = "{}/agents".format(self._base_url)
        resp = requests.post(req_url, headers=headers, data=json_pl)

        agent = self._decode_response(resp)

        return agent

    def get_agent(self, agent_id):
        if (not isinstance(agent_id, six.string_types) or
                agent_id == ""):
            raise CraftAIBadRequestError("""agent_id has to be a non-empty"""
                                         """string""")
        # No supplementary headers
        headers = self._headers.copy()

        req_url = "{}/agents/{}".format(self._base_url, agent_id)
        resp = requests.get(req_url, headers=headers)

        agent = self._decode_response(resp)

        return agent

    def delete_agent(self, agent_id):
        if (not isinstance(agent_id, six.string_types) or
                agent_id == ""):
            raise CraftAIBadRequestError("""agent_id has to be a non-empty"""
                                         """string""")
        # No supplementary headers
        headers = self._headers.copy()

        req_url = "{}/agents/{}".format(self._base_url, agent_id)
        resp = requests.delete(req_url, headers=headers)

        decoded_resp = self._decode_response(resp)

        return decoded_resp

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

    def _decode_response(self, response):
        if response.status_code == requests.codes.not_found:
            raise CraftAINotFoundError(response.text)
        if response.status_code == requests.codes.bad_request:
            raise CraftAIBadRequestError(response.text)
        if response.status_code == requests.codes.unauthorized:
            raise CraftAICredentialsError(response.text)

        try:
            return response.json()
        except json.JSONDecodeError:
            raise CraftAIUnknownError(response.text)
