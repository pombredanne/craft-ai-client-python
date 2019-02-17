import numbers
import six

from craftai.errors import CraftAiDecisionError, CraftAiNullDecisionError
from craftai.operators import OPERATORS, OPERATORS_FUNCTION
from craftai.types import TYPES
from craftai.timezones import is_timezone

_DECISION_VERSION = "2.0.0"

_VALUE_VALIDATORS = {
  TYPES["continuous"]: lambda value: isinstance(value, numbers.Real),
  TYPES["enum"]: lambda value: isinstance(value, six.string_types),
  TYPES["timezone"]: lambda value: is_timezone(value),
  TYPES["time_of_day"]: lambda value: (isinstance(value, numbers.Real)
                                       and value >= 0 and value < 24),
  TYPES["day_of_week"]: lambda value: (isinstance(value, six.integer_types)
                                       and value >= 0 and value <= 6),
  TYPES["day_of_month"]: lambda value: (isinstance(value, six.integer_types)
                                        and value >= 1 and value <= 31),
  TYPES["month_of_year"]: lambda value: (isinstance(value, six.integer_types)
                                         and value >= 1 and value <= 12)
}

##############################
## Interpreter for V2 Trees ##
##############################

class InterpreterV2(object):

  @staticmethod
  def decide(configuration, bare_tree, context):
    # Check if missing values are handled
    enable_missing_values = False if configuration.get(
      "deactivate_missing_values") is True else True

    InterpreterV2._check_context(configuration, context, enable_missing_values)

    decision_result = {}
    decision_result["output"] = {}
    for output in configuration.get("output"):
      decision_result["output"][output] = InterpreterV2._decide_recursion(bare_tree[output],
                                                                          context,
                                                                          bare_tree[output].get(
                                                                            "output_values"),
                                                                          enable_missing_values)
    decision_result["_version"] = _DECISION_VERSION
    return decision_result

  @staticmethod
  def _decide_recursion(node, context, values, enable_missing_values):
    # If we are on a leaf
    if not (node.get("children") is not None and len(node.get("children"))):
      # We check if a leaf has the key 'prediction' corresponging to a v2 tree
      prediction = node.get("prediction")
      if prediction is None:
        prediction = node

      predicted_value = prediction.get("value")
      if predicted_value is None:
        raise CraftAiNullDecisionError(
          """Unable to take decision: the decision tree has no valid"""
          """ predicted value for the given context."""
        )

      leaf = {
        "predicted_value": predicted_value,
        "confidence": prediction.get("confidence") or 0,
        "decision_rules": []
      }

      distribution = prediction.get("distribution")
      if distribution and not isinstance(distribution, list):
        standard_deviation = prediction["distribution"].get("standard_deviation")
        if standard_deviation:
          leaf["standard_deviation"] = standard_deviation

      return leaf
    # Finding the first element in this node's childrens matching the
    # operator condition with given context
    matching_child = InterpreterV2._find_matching_child(node, context, enable_missing_values)

    # If there is no child corresponding matching the operators then we compute
    # the probabilistic distribution from this node.
    if not matching_child:
      if enable_missing_values:
        result, _ = InterpreterV2._distribution(node)
        # if the given result is an array with more than an
        # element, then it means that it corresponds to a
        # distribution. Otherwise, it corresponds to the
        # distributed mean in this subtree.
        if len(result) > 1:
          final_result = {"predicted_value": values[result.index(max(result))]}
        else:
          final_result = {"predicted_value": result[0]}
        final_result["decision_rules"] = []
        final_result["confidence"] = None
        return final_result
      prop = node.get("children")[0].get("decision_rule").get("property")
      raise CraftAiNullDecisionError(
        """Unable to take decision: value '{}' for property '{}' doesn't"""
        """ validate any of the decision rules.""".format(context.get(prop), prop)
      )

    # If a matching child is found, recurse
    result = InterpreterV2._decide_recursion(matching_child, context, values, enable_missing_values)
    new_predicates = [{
      "property": matching_child["decision_rule"]["property"],
      "operator": matching_child["decision_rule"]["operator"],
      "operand": matching_child["decision_rule"]["operand"]
    }]

    final_result = {
      "predicted_value": result["predicted_value"],
      "confidence": result["confidence"],
      "decision_rules": new_predicates + result["decision_rules"]
    }

    if result.get("standard_deviation", None) is not None:
      final_result["standard_deviation"] = result.get("standard_deviation")

    return final_result

  @staticmethod
  def _distribution(node):
    # If it is a leaf
    if not (node.get("children") is not None and len(node.get("children"))):
      prediction = node.get("prediction")
      value_distribution = prediction.get("distribution")
      nb_samples = prediction["nb_samples"]
      # It is a classification problem
      if isinstance(value_distribution, list):
        return [value_distribution, nb_samples]

      # It is a regression problem
      predicted_value = prediction.get("value")
      if predicted_value is not None:
        return [[predicted_value], nb_samples]

      raise CraftAiDecisionError(
        """Unable to take decision: the decision tree has no valid"""
        """ predicted value for the given context."""
      )

    # If it is not a leaf, we recurse into the children and store
    # the distributions/means and sizes of each child branch.
    def recurse(_child):
      return InterpreterV2._distribution(_child)
    array_sizes = map(recurse, node.get("children"))
    array, sizes = zip(*array_sizes)
    mean = InterpreterV2.compute_mean(array, sizes)
    return mean, sum(sizes)


  @staticmethod
  def compute_mean(array, sizes):
    # Compute the total number of element
    total_size = float(sum(sizes))
    ratio_applied = [[x * size / total_size for x in x_array]
                     for x_array, size in zip(array, sizes)]
    return list(map(sum, zip(*ratio_applied)))

  @staticmethod
  def _find_matching_child(node, context, enable_missing_values=False):
    for child in node["children"]:
      property_name = child["decision_rule"]["property"]
      operand = child["decision_rule"]["operand"]
      operator = child["decision_rule"]["operator"]
      context_value = context.get(property_name)

      # If there is no context value:
      if context_value is None:
        if not enable_missing_values:
          raise CraftAiDecisionError(
            """Unable to take decision, property '{}' is missing from the given context.""".
            format(property_name)
          )
      if (not isinstance(operator, six.string_types) or
          not operator in OPERATORS.values()):
        raise CraftAiDecisionError(
          """Invalid decision tree format, {} is not a valid"""
          """ decision operator.""".format(operator)
        )

      # To be compared, continuous parameters should not be strings
      if TYPES["continuous"] in operator:
        context_value = float(context_value)
        operand = float(operand)
      if OPERATORS_FUNCTION[operator](context_value, operand):
        return child
    return {}

  @staticmethod
  def _check_context(configuration, context, enable_missing_values=False):
    # Extract the required properties (i.e. those that are not the output)
    expected_properties = [
      p for p in configuration["context"]
      if not p in configuration["output"]
    ]

    if not enable_missing_values:
      # Retrieve the missing properties
      missing_properties = [
        p for p in expected_properties
        if not p in context or context[p] is None
      ]
    else:
      missing_properties = []

    # Validate the values
    bad_properties = [
      p for p in expected_properties
      if not InterpreterV2.validate_property_value(configuration, context, p)
    ]

    if missing_properties or bad_properties:
      missing_properties = sorted(missing_properties)
      missing_properties_messages = [
        "expected property '{}' is not defined"
        .format(p) for p in missing_properties
      ]
      bad_properties = sorted(bad_properties)
      bad_properties_messages = [
        "'{}' is not a valid value for property '{}' of type '{}'"
        .format(context[p], p, configuration["context"][p]["type"]) for p in bad_properties
      ]

      errors = missing_properties_messages + bad_properties_messages

      # deal with missing properties
      if errors:
        message = "Unable to take decision, the given context is not valid: " + errors.pop(0)

        for error in errors:
          message = "".join((message, ", ", error))
        message = message + "."

        raise CraftAiDecisionError(message)

  @staticmethod
  def validate_property_value(configuration, context, property_name):
    if not property_name in context:
      return False

    if context[property_name] is None:
      return True

    property_type = configuration["context"][property_name]["type"]
    if property_type in _VALUE_VALIDATORS:
      property_value = context[property_name]
      return _VALUE_VALIDATORS[property_type](property_value)
    return True
