from dateutil.parser import isoparse
from nose.tools import assert_equal

from craftai import format_property, format_decision_rule


def test_format_property_time_of_day():
  formatter = format_property("time_of_day")

  assert_equal(formatter(11.5), "11:30")
  assert_equal(formatter(11.008), "11:00:28")

  assert_equal(formatter(isoparse("2016-10-20T08:20:03")), "08:20:03")
  assert_equal(formatter(isoparse("2016-08-12T13:37")), "13:37")


def test_format_property_enum():
  formatter = format_property("enum")

  assert_equal(formatter("toto"), "toto")

def test_format_property_continuous():
  formatter = format_property("continuous")

  assert_equal(formatter(12.4), "12.4")
  assert_equal(formatter(12.4234), "12.42")

def test_format_property_month_of_year():
  formatter = format_property("month_of_year")

  assert_equal(formatter(1), "Jan")
  assert_equal(formatter(6), "Jun")
  assert_equal(formatter(12), "Dec")

def test_format_decision_rule_in_time_of_day():
  assert_equal(format_decision_rule({
    "operator": "[in[",
    "operand": [11.5, 12.3],
    "type": "time_of_day"
  }), "[11:30, 12:18[")

def test_format_decision_rule_in_continuous():
  assert_equal(format_decision_rule({
    "operator": "[in[",
    "operand": [11.5, 12.3],
    "type": "continuous"
  }), "[11.5, 12.3[")

def test_format_decision_rule_in_day_of_week():
  assert_equal(format_decision_rule({
    "operator": "[in[",
    "operand": [3, 5],
    "type": "day_of_week"
  }), "Thu to Fri")

  assert_equal(format_decision_rule({
    "operator": "[in[",
    "operand": [4, 0],
    "type": "day_of_week"
  }), "Fri to Sun")

def test_format_decision_rule_in_month_of_year():
  assert_equal(format_decision_rule({
    "operator": "[in[",
    "operand": [1, 12],
    "type": "month_of_year"
  }), "Jan to Nov")

  assert_equal(format_decision_rule({
    "operator": "[in[",
    "operand": [4, 2],
    "type": "month_of_year"
  }), "Apr to Jan")

  assert_equal(format_decision_rule({
    "operator": "[in[",
    "operand": [5, 1],
    "type": "month_of_year"
  }), "May to Dec")

  assert_equal(format_decision_rule({
    "operator": "[in[",
    "operand": [5, 3],
    "type": "month_of_year"
  }), "May to Feb")

def test_format_decision_rule_gte_continuous():
  assert_equal(format_decision_rule({
    "operator": ">=",
    "operand": 3.14,
    "type": "continuous"
  }), ">= 3.14")

def test_format_decision_rule_gte_enum():
  assert_equal(format_decision_rule({
    "operator": ">=",
    "operand": "foo",
    "type": "enum"
  }), ">= foo")

def test_format_decision_rule_lt_continuous():
  assert_equal(format_decision_rule({
    "operator": "<",
    "operand": 666,
    "type": "continuous"
  }), "< 666")

def test_format_decision_rule_lt_timezone():
  assert_equal(format_decision_rule({
    "operator": "<",
    "operand": "+02:00",
    "type": "timezone"
  }), "< +02:00")

def test_format_decision_rule_is_continuous():
  assert_equal(format_decision_rule({
    "operator": "is",
    "operand": 5637,
    "type": "continuous"
  }), "is 5637")

def test_format_decision_rule_is_enum():
  assert_equal(format_decision_rule({
    "operator": "is",
    "operand": "abracadabra",
    "type": "enum"
  }), "is abracadabra")
