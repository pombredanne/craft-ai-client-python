import six
import re

from craftai.errors import *
from craftai.operators import _OPERATORS
from craftai.time import Time

class Interpreter(object):

  @staticmethod
  def decide(tree, args):
    bare_tree, configuration, version = Interpreter._parse_tree(tree)
    if configuration != {}:
        state = args[0]
        time = None if len(args) == 1 else args[1]
        context = Interpreter._rebuild_context(configuration, state, time)
    else:
        context = Interpreter.join_decide_args(args)
    # self._check_context(configuration, context, version)
    raw_decision = Interpreter._decide_recursion(bare_tree, context)

    # If the configuration is not included in the tree object (f.i. version 0.0.1)
    # we give a default key name to the output
    try:
        output_name = configuration.get("output")[0]
    except TypeError:
        output_name = "value"

    decision = {}
    decision["decision"] = {}
    decision["decision"][output_name] = raw_decision["value"]
    if raw_decision.get("standard_deviation", None) is not None:
        decision["decision"]["standard_deviation"] = raw_decision.get("standard_deviation")
    decision["confidence"] = raw_decision["confidence"]
    decision["predicates"] = raw_decision["predicates"]
    decision["context"] = context

    return decision

  ####################
  # Internal helpers #
  ####################

  @staticmethod
  def _rebuild_context(configuration, state, time=None):
      # Model should come from _parse_tree and is assumed to be checked upon
      # already
      mo = configuration["output"]
      mc = configuration["context"]

      # We should not use the output key(s) to compare against
      configuration_ctx = {
          key: mc[key] for (key, value) in mc.items() if (key not in mo)
      }

      # Check if we need the time object
      to_generate = []
      for prop in configuration_ctx.items():
          prop_name = prop[0]
          prop_attributes = prop[1]
          if prop_attributes["type"] in ["time_of_day", "day_of_week", "day_of_month", "month_of_year", "timezone"]:
              # case 1: is_generated is at True, we must generate the time for the associated context property
              # case 2: is_generated is not given, by default at True, so we must generate it as well
              case_1 = "is_generated" in prop_attributes.keys() and prop[1]["is_generated"] == True
              case_2 = "is_generated" not in prop_attributes.keys()
              if case_1 or case_2:
                to_generate.append(prop_name)

      # Raise an exception if a time object is not provided but needed
      if (not isinstance(time, Time)) and len(to_generate) > 0:

          # Check for missings (not provided and need to be generated)
          missings = []
          for prop in to_generate:
              if prop_name not in state.keys():
                  missings.append(prop_name)

          # Raise an error if some need to be generated but not provided and no Time object
          if len(missings) > 0:
              raise CraftAIDecisionError(
                """you must provide a Time object to decide() because"""
                """ context properties {} need to be generated.""".format(missings)
              )
          else:
              to_generate = []

      # Generate context properties which need to
      if len(to_generate) > 0:
          for prop in to_generate:
              state[prop] = time.to_dict()[configuration_ctx[prop]["type"]]

      # Rebuild the context with generated and non-generated values
      context = {
          feature: state.get(feature) for feature, properties in configuration_ctx.items()
      }

      return context

  @staticmethod
  def _decide_recursion(node, context):
    # If we are on a leaf
    if not node.get("predicate_property"):
      return {
        "value": node["value"],
        "confidence": node.get("confidence") or 0,
        "standard_deviation": node.get("standard_deviation", None),
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
    matching_child = Interpreter._find_matching_child(node, ctx_value, prop_name)

    if not matching_child:
      raise CraftAIDecisionError(
        """Invalid decision tree format, no leaf matching the given"""
        """ context could be found because the tree is malformed."""
      )

    # If a matching child is found, recurse
    result = Interpreter._decide_recursion(matching_child, context)
    new_predicates = [{
      "property": prop_name,
      "op": matching_child["predicate"]["op"],
      "value": matching_child["predicate"]["value"]
    }]
    return {
      "value": result["value"],
      "confidence": result["confidence"],
      "standard_deviation": result.get("standard_deviation", None),
      "predicates": new_predicates + result["predicates"]
    }

  @staticmethod
  def _find_matching_child(node, context, prop_name):
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

  @staticmethod
  def join_decide_args(args):
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

  @staticmethod
  def _parse_tree(tree_object):
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
    if re.compile('\d+.\d+.\d+').match(tree_version) is None:
      raise CraftAIDecisionError(
        """Invalid decision tree format, {} is not a valid version.""".
        format(tree_version)
      )
    elif tree_version == "0.0.1":
      if len(tree_object) < 2:
        raise CraftAIDecisionError(
          """Invalid decision tree format, no tree found."""
        )
      bare_tree = tree_object[1]
      configuration = {}
    elif tree_version == "0.0.2":
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
      configuration = tree_object[1]["model"]
    elif tree_version == "0.0.3":
      if (len(tree_object) < 2 or
            not tree_object[1]):
        raise CraftAIDecisionError(
            """Invalid decision tree format, no configuration found"""
        )
      if len(tree_object) < 3:
        raise CraftAIDecisionError(
          """Invalid decision tree format, no tree found."""
        )
      bare_tree = tree_object[2]
      configuration = tree_object[1]
    elif tree_version == "0.0.4":
      if (len(tree_object) < 2 or
            not tree_object[1]):
        raise CraftAIDecisionError(
            """Invalid decision tree format, no configuration found"""
        )
      if len(tree_object) < 3:
        raise CraftAIDecisionError(
          """Invalid decision tree format, no tree found."""
        )
      bare_tree = tree_object[2]
      configuration = tree_object[1]
    else:
      raise CraftAIDecisionError(
        """Invalid decision tree format, {} is not a supported"""
        """ version.""".
        format(tree_version)
      )
    return bare_tree, configuration, tree_version
