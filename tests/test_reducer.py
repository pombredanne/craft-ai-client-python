from nose.tools import assert_raises, assert_equal

from craftai import reduce_decision_rules, errors

def test_reduce_decision_rules_is_is():
  rules = [
    {"property": "test", "operator": "is", "operand": "toto"},
    {"property": "test", "operator": "is", "operand": "toto"}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "is", "operand": "toto"}
  ])

def test_reduce_decision_rules_is():
  rules = [
    {"property": "test", "operator": "is", "operand": "toto"}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "is", "operand": "toto"}
  ])

def test_reduce_decision_rules_is_in():
  rules = [
    {"property": "test", "operator": "is", "operand": "toto"},
    {"property": "test", "operator": "[in[", "operand": "titi"}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)

def test_reduce_decision_rules_is_is_diff_operands():
  rules = [
    {"property": "test", "operator": "is", "operand": "toto"},
    {"property": "test", "operator": "is", "operand": "titi"}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)

def test_reduce_decision_rules_in_in_1():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [0, 13]},
    {"property": "test", "operator": "[in[", "operand": [2, 12]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [2, 12]}
  ])

def test_reduce_decision_rules_in_in_2():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [0, 13]},
    {"property": "test", "operator": "[in[", "operand": [2, 16]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [2, 13]}
  ])

def test_reduce_decision_rules_in_in_3():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [1, 13]},
    {"property": "test", "operator": "[in[", "operand": [0, 12]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [1, 12]}
  ])

def test_reduce_decision_rules_in_in_dow():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [5, 3]},
    {"property": "test", "operator": "[in[", "operand": [2, 3]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [2, 3]}
  ])

def test_reduce_decision_rules_in_in_dom():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [5, 4]},
    {"property": "test", "operator": "[in[", "operand": [12, 1]},
    {"property": "test", "operator": "[in[", "operand": [12, 16]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [12, 16]}
  ])

def test_reduce_decision_rules_in_in_self():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [3, 4]},
    {"property": "test", "operator": "[in[", "operand": [3, 4]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [3, 4]}
  ])

def test_reduce_decision_rules_in_in_self_p():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [4, 2]},
    {"property": "test", "operator": "[in[", "operand": [4, 2]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [4, 2]}
  ])

def test_reduce_decision_rules_in_in_pnp_invalid_1():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [15, 20]},
    {"property": "test", "operator": "[in[", "operand": [22, 14]}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)

def test_reduce_decision_rules_in_in_pnp_invalid_2():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [15, 20]},
    {"property": "test", "operator": "[in[", "operand": [22, 25]}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)

def test_reduce_decision_rules_in():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [1, 13]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [1, 13]}
  ])

def test_reduce_decision_rules_in_is():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [1, 13]},
    {"property": "test", "operator": "is", "operand": "toto"}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)

def test_reduce_decision_rules_in_lt():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [1, 13]},
    {"property": "test", "operator": "<", "operand": 2}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [1, 2]}
  ])

def test_reduce_decision_rules_in_gte():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [1, 13]},
    {"property": "test", "operator": ">=", "operand": 12}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [12, 13]}
  ])

def test_reduce_decision_rules_in_lt_gte():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [1, 13]},
    {"property": "test", "operator": "<", "operand": 12},
    {"property": "test", "operator": ">=", "operand": 2}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [2, 12]}
  ])

def test_reduce_decision_rules_in_in_p():
  rules = [
    {"property": "test", "operator": "[in[", "operand": [23, 3]},
    {"property": "test", "operator": "[in[", "operand": [22, 2]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [23, 2]}
  ])

def test_reduce_decision_rules_lt_lt_1():
  rules = [
    {"property": "test", "operator": "<", "operand": 2},
    {"property": "test", "operator": "<", "operand": 6}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "<", "operand": 2}
  ])

def test_reduce_decision_rules_lt_lt_2():
  rules = [
    {"property": "test", "operator": "<", "operand": 2},
    {"property": "test", "operator": "<", "operand": 2}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "<", "operand": 2}
  ])

def test_reduce_decision_rules_lt():
  rules = [
    {"property": "test", "operator": "<", "operand": 2}
  ]
  assert_equal(reduce_decision_rules(rules), rules)

def test_reduce_decision_rules_lt_in():
  rules = [
    {"property": "test", "operator": "<", "operand": 2},
    {"property": "test", "operator": "[in[", "operand": [1, 13]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [1, 2]}
  ])

def test_reduce_decision_rules_lt_gte():
  rules = [
    {"property": "test", "operator": "<", "operand": 13},
    {"property": "test", "operator": ">=", "operand": 2}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [2, 13]}
  ])

def test_reduce_decision_rules_lt_gte_complex():
  rules = [
    {"property": "test", "operator": "<", "operand": 650},
    {"property": "test", "operator": ">=", "operand": 232.82},
    {"property": "test", "operator": "<", "operand": 251.99},
    {"property": "test", "operator": "<", "operand": 345.22}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [232.82, 251.99]}
  ])

def test_reduce_decision_rules_gte_1():
  rules = [
    {"property": "test", "operator": ">=", "operand": 4},
    {"property": "test", "operator": ">=", "operand": 2}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": ">=", "operand": 4}
  ])

def test_reduce_decision_rules_gte_2():
  rules = [
    {"property": "test", "operator": ">=", "operand": 2}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": ">=", "operand": 2}
  ])

def test_reduce_decision_rules_gte_gte_self():
  rules = [
    {"property": "test", "operator": ">=", "operand": 2},
    {"property": "test", "operator": ">=", "operand": 2}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": ">=", "operand": 2}
  ])

def test_reduce_decision_rules_gte_in():
  rules = [
    {"property": "test", "operator": ">=", "operand": 2},
    {"property": "test", "operator": "[in[", "operand": [1, 13]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [2, 13]}
  ])

def test_reduce_decision_rules_gte_lt():
  rules = [
    {"property": "test", "operator": ">=", "operand": 2},
    {"property": "test", "operator": "<", "operand": 13}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "test", "operator": "[in[", "operand": [2, 13]}
  ])

def test_reduce_decision_rules_gte_lt_bad():
  rules = [
    {"property": "test", "operator": ">=", "operand": 13},
    {"property": "test", "operator": "<", "operand": 2}
  ]
  assert_raises(errors.CraftAiError,
                reduce_decision_rules,
                rules)


def test_reduce_decision_rules_2_properties():
  rules = [
    {"property": "a", "operator": ">=", "operand": 2},
    {"property": "b", "operator": "[in[", "operand": [23, 3]},
    {"property": "a", "operator": "<", "operand": 13},
    {"property": "b", "operator": "[in[", "operand": [22, 2]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "a", "operator": "[in[", "operand": [2, 13]},
    {"property": "b", "operator": "[in[", "operand": [23, 2]}
  ])


def test_reduce_decision_rules_3_properties():
  rules = [
    {"property": "b", "operator": "[in[", "operand": [23, 3]},
    {"property": "a", "operator": ">=", "operand": 2},
    {"property": "c", "operator": "<", "operand": 2},
    {"property": "a", "operator": "<", "operand": 13},
    {"property": "b", "operator": "[in[", "operand": [22, 2]}
  ]
  assert_equal(reduce_decision_rules(rules), [
    {"property": "b", "operator": "[in[", "operand": [23, 2]},
    {"property": "a", "operator": "[in[", "operand": [2, 13]},
    {"property": "c", "operator": "<", "operand": 2}
  ])
