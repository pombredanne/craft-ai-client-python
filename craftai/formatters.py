import datetime
import math

from craftai.errors import CraftAiError
from craftai.operators import OPERATORS
from craftai.types import TYPES, TYPE_ANY

DAYS = [
  "Mon",
  "Tue",
  "Wed",
  "Thu",
  "Fri",
  "Sat",
  "Sun"
]

MONTHS = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec"
]

def _time_formatter(time):
  if isinstance(time, datetime.datetime):
    if time.second == 0:
      return time.strftime("%H:%M")
    return time.strftime("%H:%M:%S")
  else:
    hours = math.floor(time)
    dec_minutes = (time - hours) * 60
    minutes = math.floor(dec_minutes)
    seconds = math.floor((dec_minutes - minutes) * 60)

    if seconds > 0:
      return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return "{:02d}:{:02d}".format(hours, minutes)

PROPERTY_FORMATTER = {
  TYPE_ANY: lambda value: value,
  TYPES["continuous"]: lambda number: "{:.2f}".format(number).rstrip("0").rstrip("."),
  TYPES["time_of_day"]: _time_formatter,
  TYPES["day_of_week"]: lambda day: DAYS[day.weekday()]
                        if isinstance(day, datetime.datetime)
                        else DAYS[day],
  TYPES["day_of_month"]: lambda day: day.day if isinstance(day, datetime.datetime) else day,
  # Months are in [1; 12] thus -1 to be index month name in [0; 11]
  TYPES["month_of_year"]: lambda month: MONTHS[month.month - 1]
                          if isinstance(month, datetime.datetime)
                          else MONTHS[month - 1]
}

def format_property(property_type, value=None):
  formatter = (PROPERTY_FORMATTER[property_type] if property_type in PROPERTY_FORMATTER
               else PROPERTY_FORMATTER[TYPE_ANY])
  if value is not None:
    return formatter(value)
  return formatter

def _in_day_of_week_formatter(operand, operand_formatter):
  day_from = math.floor(operand[0])
  day_to = math.floor(operand[1])
  if ((day_to - day_from == 1) or (day_from == 6 and day_to == 0)):
    # One day in the interval
    return operand_formatter(day_from)
  return "{} to {}".format(operand_formatter(day_from), operand_formatter((7 + day_to - 1) % 7))

def _in_month_of_year_formatter(operand, operand_formatter):
  month_from = math.floor(operand[0])
  month_to = math.floor(operand[1])
  if ((month_to - month_from == 1) or (month_from == 12 and month_to == 1)):
    # One month in the interval
    return operand_formatter(month_from)
  return "{} to {}".format(operand_formatter(month_from),
                           operand_formatter((12 + month_to - 1) % 12))


FORMATTER_FROM_DECISION_RULE = {
  OPERATORS["IS"]: {
    TYPE_ANY: lambda operand, formatter: "is {}".format(formatter(operand))
  },
  OPERATORS["IN"]: {
    TYPE_ANY: lambda operand, formatter: "[{}, {}[".format(formatter(operand[0]),
                                                           formatter(operand[1])),
    TYPES["day_of_week"]: _in_day_of_week_formatter,
    TYPES["day_of_month"]: lambda operand, formatter: "[{}, {}[".format(formatter(operand[0]),
                                                                        formatter(operand[1])),
    TYPES["month_of_year"]: _in_month_of_year_formatter
  },
  OPERATORS["GTE"]: {
    TYPE_ANY: lambda operand, formatter: ">= {}".format(formatter(operand))
  },
  OPERATORS["LT"]: {
    TYPE_ANY: lambda operand, formatter: "< {}".format(formatter(operand))
  }
}

def format_decision_rule(rule):
  if rule["operator"] not in FORMATTER_FROM_DECISION_RULE:
    raise CraftAiError("Unable to format the given decision rule: unknown operator '{}'."
                       .format(rule["operator"]))
  operator_formatters = FORMATTER_FROM_DECISION_RULE[rule["operator"]]

  operand_type = rule["type"] if "type" in rule else TYPE_ANY

  formatter = (operator_formatters[operand_type] if operand_type in operator_formatters
               else operator_formatters[TYPE_ANY])
  operand_formatter = format_property(operand_type)
  return formatter(rule["operand"], operand_formatter)
