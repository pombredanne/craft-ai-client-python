OPERATORS = {
  "IS": "is",
  "IN": "[in[",
  "GTE": ">=",
  "LT": "<",
}

LT = lambda a, b: a < b
GTE = lambda a, b: a >= b

OPERATORS_FUNCTION = {
  OPERATORS["IS"]: lambda context, value: context == value,
  OPERATORS["GTE"]: lambda context, value: safe_op(context, value, GTE),
  OPERATORS["LT"]: lambda context, value: safe_op(context, value, LT),
  OPERATORS["IN"]: lambda context, value:
                   safe_op(context, value[0], GTE) and
                   safe_op(context, value[1], LT) if safe_op(value[0], value[1], LT)
                   else safe_op(context, value[0], GTE) or safe_op(context, value[1], LT)
}

def safe_op(context, value, func):
  if context is not None and context != {}:
    return func(context, value)
  return False
