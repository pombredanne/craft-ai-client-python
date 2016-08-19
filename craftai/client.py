import requests
import json
import six

import semantic_version as semver

from craftai import helpers

from craftai.errors import *
from craftai.operators import _OPERATORS
from craftai.time import Time


class CraftAIClient(object):
    """Client class for craft ai's API"""

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
        cfg = cfg.copy()
        if (not isinstance(cfg.get("token"), six.string_types)):
            raise CraftAICredentialsError("""Unable to create client with no"""
                                          """ or invalid token provided.""")
        if (not isinstance(cfg.get("owner"), six.string_types)):
            raise CraftAICredentialsError("""Unable to create client with no"""
                                          """ or invalid owner provided.""")
        if (not isinstance(cfg.get("url"), six.string_types)):
            cfg["url"] = "https://beta.craft.ai"
        if cfg.get("url").endswith("/"):
            raise CraftAIBadRequestError("""Unable to create client with"""
                                         """invalid url provided. The url """
                                         """should not terminate with a """
                                         """slash. """)
        self._config = cfg

        self._base_url = "{}/api/{}".format(
            self.config["url"],
            self.config["owner"])

        # Headers have to be reset here to avoid multiple definitions
        # of the 'Authorization' header if config is modified
        self._headers = {}
        self._headers["Authorization"] = "Bearer " + self.config.get("token")

    #################
    # Agent methods #
    #################

    def create_agent(self, model, agent_id=""):
        # Building final headers
        ct_header = {"Content-Type": "application/json; charset=utf-8"}
        headers = helpers.join_dicts(self._headers, ct_header)

        # Building payload and checking that it is valid for a JSON
        # serialization
        payload = {
            "id": agent_id,
            "model": model
        }
        try:
            json_pl = json.dumps(payload)
        except TypeError as e:
            raise CraftAIBadRequestError("Invalid model or agent id given. {}".
                                         format(e.__str__())
                                         )

        req_url = "{}/agents".format(self._base_url)
        resp = requests.post(req_url, headers=headers, data=json_pl)

        agent = self._decode_response(resp)

        return agent

    def get_agent(self, agent_id):
        # Raises an error when agent_id is invalid
        self._check_agent_id(agent_id)

        # No supplementary headers needed
        headers = self._headers.copy()

        req_url = "{}/agents/{}".format(self._base_url, agent_id)
        resp = requests.get(req_url, headers=headers)

        agent = self._decode_response(resp)

        return agent

    def delete_agent(self, agent_id):
        # Raises an error when agent_id is invalid
        self._check_agent_id(agent_id)

        # No supplementary headers needed
        headers = self._headers.copy()

        req_url = "{}/agents/{}".format(self._base_url, agent_id)
        resp = requests.delete(req_url, headers=headers)

        decoded_resp = self._decode_response(resp)

        return decoded_resp

    ###################
    # Context methods #
    ###################

    def add_operations(self, agent_id, operations):
        # Raises an error when agent_id is invalid
        self._check_agent_id(agent_id)

        # Building final headers
        ct_header = {"Content-Type": "application/json; charset=utf-8"}
        headers = helpers.join_dicts(self._headers, ct_header)

        try:
            json_pl = json.dumps(operations)
        except TypeError as e:
            raise CraftAIBadRequestError("Invalid model or agent id given. {}".
                                         format(e.__str__())
                                         )

        req_url = "{}/agents/{}/context".format(self._base_url, agent_id)
        resp = requests.post(req_url, headers=headers, data=json_pl)

        decoded_resp = self._decode_response(resp)

        return decoded_resp

    def get_operations_list(self, agent_id):
        # Raises an error when agent_id is invalid
        self._check_agent_id(agent_id)

        headers = self._headers.copy()

        req_url = "{}/agents/{}/context".format(self._base_url, agent_id)

        resp = requests.get(req_url, headers=headers)

        ops_list = self._decode_response(resp)

        return ops_list

    def get_context_state(self, agent_id, timestamp):
        # Raises an error when agent_id is invalid
        self._check_agent_id(agent_id)

        headers = self._headers.copy()

        req_url = "{}/agents/{}/context/state?t={}".format(
            self._base_url,
            agent_id,
            timestamp)
        resp = requests.get(req_url, headers=headers)

        context_state = self._decode_response(resp)

        return context_state

    #########################
    # Decision tree methods #
    #########################

    def get_decision_tree(self, agent_id, timestamp):
        # Raises an error when agent_id is invalid
        self._check_agent_id(agent_id)

        headers = self._headers.copy()

        req_url = "{}/agents/{}/decision/tree?t={}".format(
            self._base_url,
            agent_id,
            timestamp)

        resp = requests.get(req_url, headers=headers)

        decision_tree = self._decode_response(resp)

        return decision_tree

    def decide(self, tree, *args):
        bare_tree, model, version = self._parse_tree(tree)
        if model != {}:
            context = self._rebuild_context(model, args)
        else:
            context = self._join_decide_args(args)
        # self._check_context(model, context, version)
        raw_decision = self._decide_recursion(bare_tree, context)

        # If the model is not included in the tree object (f.i. version 0.0.1)
        # we give a default key name to the output
        try:
            output_name = model.get("output")[0]
        except TypeError:
            output_name = "value"

        decision = {}
        decision["decision"] = {}
        decision["decision"][output_name] = raw_decision["value"]
        decision["confidence"] = raw_decision["confidence"]
        decision["predicates"] = raw_decision["predicates"]
        decision["context"] = context

        return decision

    ####################
    # Internal helpers #
    ####################

    def _rebuild_context(self, model, args):
        # Model should come from _parse_tree and is assumed to be checked upon
        # already
        mo = model["output"]
        mc = model["context"]

        # We should not use the output key(s) to compare against
        model_ctx = {
            key: mc[key] for (key, value) in mc.items() if (key not in mo)
        }

        context = {}
        for arg in args:
            if not arg:
                continue
            context.update({
                k: self._context_value(k, v, arg) for k, v in model_ctx.items()
            })

        return context

    def _context_value(self, k, v, arg):
        if isinstance(arg, Time):
            time_of_day = arg.to_dict()["time_of_day"]
            day_of_week = arg.to_dict()["day_of_week"]
            timezone = arg.to_dict()["timezone"]

            if (v["type"] == "day_of_week" and
                    (v.get("is_generated") is None or v["is_generated"])):
                return day_of_week
            elif (v["type"] == "time_of_day" and
                    (v.get("is_generated") is None or v["is_generated"])):
                return time_of_day
            elif v["type"] == "timezone":
                return timezone
            else:
                return None
        else:
            return arg.get(k)

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

    def _check_agent_id(self, agent_id):
        """Checks that the given agent_id is a valid non-empty string.

        Raises an error if the given agent_id is not of type string or if it is
        an empty string.
        """
        if (not isinstance(agent_id, six.string_types) or
                agent_id == ""):
            raise CraftAIBadRequestError("""agent_id has to be a non-empty"""
                                         """string""")

    def _decide_recursion(self, node, context):
        # If we are on a leaf
        if not node.get("predicate_property"):
            return {
                "value": node["value"],
                "confidence": node.get("confidence") or 0,
                "predicates": []
            }

        # If we are on a regular node
        prop_name = node["predicate_property"]

        ctx_value = context.get(prop_name)
        if ctx_value is None:
            raise CraftAIDecisionError(
                """Property '{}' is not defined in the given context""".
                format(prop_name)
            )

        # Finding the first element in this node's childrens matching the
        # operator condition with given context
        matching_child = self._find_matching_child(node, ctx_value, prop_name)

        if not matching_child:
            raise CraftAIDecisionError(
                """Invalid decision tree format, no leaf matching the given"""
                """ context could be found because the tree is malformed."""
            )

        # If a matching child is found, recurse
        result = self._decide_recursion(matching_child, context)
        new_predicates = [{
            "property": prop_name,
            "op": matching_child["predicate"]["op"],
            "value": matching_child["predicate"]["value"]
        }]
        return {
            "value": result["value"],
            "confidence": result["confidence"],
            "predicates": new_predicates + result["predicates"]
        }

    def _find_matching_child(self, node, context, prop_name):
        for child in node["children"]:
            threshold = child["predicate"]["value"]
            operator = child["predicate"]["op"]
            if (not isinstance(operator, six.string_types) or
                    not (operator in _OPERATORS)):
                raise CraftAIDecisionError(
                    """Invalid decision tree format, {} is not a valid"""
                    """decision operator.""".
                    format(operator)
                )

            # To be compared, continuous parameters should not be strings
            if "continuous" in operator:
                context = float(context)
                threshold = float(threshold)

            if _OPERATORS[operator](context, threshold):
                return child
        return {}

    def _join_decide_args(self, args):
        joined_args = {}
        for arg in args:
            if isinstance(arg, Time):
                joined_args.update(arg.to_dict())
            try:
                joined_args.update(arg)
            except TypeError:
                raise CraftAIDecisionError(
                    """Invalid context args, the given objects aren't dicts"""
                    """ or Time instances."""
                )
        return joined_args

    def _parse_tree(self, tree_object):
        # Checking definition of tree_object
        if not (tree_object and isinstance(tree_object, list)):
            raise CraftAIDecisionError(
                """Invalid decision tree format, the given object is not a"""
                """ list or is empty."""
            )

        # Checking version existence
        tree_version = tree_object[0].get("version")
        if not tree_version:
            raise CraftAIDecisionError(
                """Invalid decision tree format, unable to find the version"""
                """ information."""
            )

        # Checking version and tree validity according to version
        if not semver.validate(tree_version):
            raise CraftAIDecisionError(
                """Invalid decision tree format, {} is not a valid version.""".
                format(tree_version)
            )
        elif semver.Version(tree_version) == semver.Version("0.0.1"):
            if len(tree_object) < 2:
                raise CraftAIDecisionError(
                    """Invalid decision tree format, no tree found."""
                )
            bare_tree = tree_object[1]
            model = {}
        elif semver.Version(tree_version) == semver.Version("0.0.2"):
            if (len(tree_object) < 2 or
                    not tree_object[1].get("model")):
                raise CraftAIDecisionError(
                    """Invalid decision tree format, no model found"""
                )
            if len(tree_object) < 3:
                raise CraftAIDecisionError(
                    """Invalid decision tree format, no tree found."""
                )
            bare_tree = tree_object[2]
            model = tree_object[1]["model"]
        elif semver.Version(tree_version) == semver.Version("0.0.3"):
            if (len(tree_object) < 2 or
                    not tree_object[1]):
                raise CraftAIDecisionError(
                    """Invalid decision tree format, no model found"""
                )
            if len(tree_object) < 3:
                raise CraftAIDecisionError(
                    """Invalid decision tree format, no tree found."""
                )
            bare_tree = tree_object[2]
            model = tree_object[1]
        else:
            raise CraftAIDecisionError(
                """Invalid decision tree format, {} is not a supported"""
                """ version.""".
                format(tree_version)
            )

        return bare_tree, model, tree_version
