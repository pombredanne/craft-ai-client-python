from nose.tools import assert_raises, assert_equal

from craftai import reduce_decision_rules, errors

def test_reduce_decision_rules_is_is():
  rules = [
    {"operator": "is", "operand": "toto"},
    {"operator": "is", "operand": "toto"}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "is")
  assert_equal(output["operand"], "toto")

def test_reduce_decision_rules_is():
  rules = [
    {"operator": "is", "operand": "toto"}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "is")
  assert_equal(output["operand"], "toto")

def test_reduce_decision_rules_is_in():
  rules = [
    {"operator": "is", "operand": "toto"},
    {"operator": "[in[", "operand": "titi"}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)

def test_reduce_decision_rules_is_is_diff_operands():
  rules = [
    {"operator": "is", "operand": "toto"},
    {"operator": "is", "operand": "titi"}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)

def test_reduce_decision_rules_in_in_1():
  rules = [
    {"operator": "[in[", "operand": [0, 13]},
    {"operator": "[in[", "operand": [2, 12]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [2, 12])

def test_reduce_decision_rules_in_in_2():
  rules = [
    {"operator": "[in[", "operand": [0, 13]},
    {"operator": "[in[", "operand": [2, 16]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [2, 13])

def test_reduce_decision_rules_in_in_3():
  rules = [
    {"operator": "[in[", "operand": [1, 13]},
    {"operator": "[in[", "operand": [0, 12]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [1, 12])

def test_reduce_decision_rules_in_in_dow():
  rules = [
    {"operator": "[in[", "operand": [5, 3]},
    {"operator": "[in[", "operand": [2, 3]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [2, 3])

def test_reduce_decision_rules_in_in_dom():
  rules = [
    {"operator": "[in[", "operand": [5, 4]},
    {"operator": "[in[", "operand": [12, 1]},
    {"operator": "[in[", "operand": [12, 16]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [12, 16])

def test_reduce_decision_rules_in_in_self():
  rules = [
    {"operator": "[in[", "operand": [3, 4]},
    {"operator": "[in[", "operand": [3, 4]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [3, 4])

def test_reduce_decision_rules_in_in_self_p():
  rules = [
    {"operator": "[in[", "operand": [4, 2]},
    {"operator": "[in[", "operand": [4, 2]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [4, 2])

def test_reduce_decision_rules_in_in_pnp_invalid_1():
  rules = [
    {"operator": "[in[", "operand": [15, 20]},
    {"operator": "[in[", "operand": [22, 14]}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)

def test_reduce_decision_rules_in_in_pnp_invalid_2():
  rules = [
    {"operator": "[in[", "operand": [15, 20]},
    {"operator": "[in[", "operand": [22, 25]}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)

def test_reduce_decision_rules_in():
  rules = [
    {"operator": "[in[", "operand": [1, 13]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [1, 13])

def test_reduce_decision_rules_in_is():
  rules = [
    {"operator": "[in[", "operand": [1, 13]},
    {"operator": "is", "operand": "toto"}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)

def test_reduce_decision_rules_in_lt():
  rules = [
    {"operator": "[in[", "operand": [1, 13]},
    {"operator": "<", "operand": 2}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [1, 2])

def test_reduce_decision_rules_in_gte():
  rules = [
    {"operator": "[in[", "operand": [1, 13]},
    {"operator": ">=", "operand": 12}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [12, 13])

def test_reduce_decision_rules_in_lt_gte():
  rules = [
    {"operator": "[in[", "operand": [1, 13]},
    {"operator": "<", "operand": 12},
    {"operator": ">=", "operand": 2}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [2, 12])

def test_reduce_decision_rules_in_in_p():
  rules = [
    {"operator": "[in[", "operand": [23, 3]},
    {"operator": "[in[", "operand": [22, 2]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [23, 2])

def test_reduce_decision_rules_lt_lt_1():
  rules = [
    {"operator": "<", "operand": 2},
    {"operator": "<", "operand": 6}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "<")
  assert_equal(output["operand"], 2)

def test_reduce_decision_rules_lt_lt_2():
  rules = [
    {"operator": "<", "operand": 2},
    {"operator": "<", "operand": 2}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "<")
  assert_equal(output["operand"], 2)

def test_reduce_decision_rules_lt():
  rules = [
    {"operator": "<", "operand": 2}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "<")
  assert_equal(output["operand"], 2)

def test_reduce_decision_rules_lt_in():
  rules = [
    {"operator": "<", "operand": 2},
    {"operator": "[in[", "operand": [1, 13]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [1, 2])

def test_reduce_decision_rules_lt_gte():
  rules = [
    {"operator": "<", "operand": 13},
    {"operator": ">=", "operand": 2}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [2, 13])

def test_reduce_decision_rules_lt_gte_complex():
  rules = [
    {"operator": "<", "operand": 650},
    {"operator": ">=", "operand": 232.82},
    {"operator": "<", "operand": 251.99},
    {"operator": "<", "operand": 345.22}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [232.82, 251.99])

def test_reduce_decision_rules_gte_1():
  rules = [
    {"operator": ">=", "operand": 4},
    {"operator": ">=", "operand": 2}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], ">=")
  assert_equal(output["operand"], 4)

def test_reduce_decision_rules_gte_2():
  rules = [
    {"operator": ">=", "operand": 2}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], ">=")
  assert_equal(output["operand"], 2)

def test_reduce_decision_rules_gte_gte_self():
  rules = [
    {"operator": ">=", "operand": 2},
    {"operator": ">=", "operand": 2}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], ">=")
  assert_equal(output["operand"], 2)

def test_reduce_decision_rules_gte_in():
  rules = [
    {"operator": ">=", "operand": 2},
    {"operator": "[in[", "operand": [1, 13]}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [2, 13])

def test_reduce_decision_rules_gte_lt():
  rules = [
    {"operator": ">=", "operand": 2},
    {"operator": "<", "operand": 13}
  ]
  output = reduce_decision_rules(rules)
  assert_equal(output["operator"], "[in[")
  assert_equal(output["operand"], [2, 13])

def test_reduce_decision_rules_gte_lt_bad():
  rules = [
    {"operator": ">=", "operand": 13},
    {"operator": "<", "operand": 2}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)
