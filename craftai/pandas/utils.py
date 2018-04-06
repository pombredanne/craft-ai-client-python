import pandas as pd

def is_valid_property_value(value):
  # From https://stackoverflow.com/a/19773559
  return (not hasattr(value, "__len__") or isinstance(value, str)) and pd.notnull(value)
