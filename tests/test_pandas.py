import pandas as pd
import numpy as np

from numpy.random import randn
from nose.tools import assert_equal, assert_raises, with_setup

import craftai.pandas

from . import settings

AGENT_ID = "test_pandas_" + settings.RUN_ID
SIMPLE_AGENT_CONFIGURATION = {
  "context": {
    "a": {
      "type": "continuous"
    },
    "b": {
      "type": "continuous"
    },
    "c": {
      "type": "continuous"
    },
    "d": {
      "type": "continuous"
    },
    "e": {
      "type": "continuous"
    }
  },
  "output": ["a"],
  "time_quantum": 100
}
SIMPLE_AGENT_DATA = pd.DataFrame(
  randn(300, 5),
  columns=["a", "b", "c", "d", "e"],
  index=pd.date_range("20130101", periods=300, freq="T").tz_localize("Europe/Paris")
)
COMPLEX_AGENT_CONFIGURATION = {
  "context": {
    "a": {
      "type": "continuous"
    },
    "b": {
      "type": "enum"
    },
    "timezone": {
      "type": "timezone"
    }
  },
  "output": ["b"],
  "time_quantum": 100
}
COMPLEX_AGENT_CONFIGURATION_2 = {
  "context": {
    "a": {
      "type": "continuous"
    },
    "b": {
      "type": "enum"
    },
    "timezone": {
      "type": "timezone"
    }
  },
  "output": ["a"],
  "time_quantum": 100
}
COMPLEX_AGENT_DATA = pd.DataFrame(
  [
    [1, "Pierre", "+02:00"],
    [2, "Paul"],
    [3],
    [4],
    [5, "Jacques"],
    [6],
    [7],
    [8, np.nan, "+01:00"],
    [9],
    [10]
  ],
  columns=["a", "b", "timezone"],
  index=pd.date_range("20130101", periods=10, freq="D").tz_localize("Europe/Paris")
)
COMPLEX_AGENT_DATA_2 = pd.DataFrame(
  [
    [1, "Pierre", "+02:00", [8, 9]],
    [2, "Paul"],
    [3],
    [4],
    [5, "Jacques"],
    [6],
    [7],
    [8, np.nan, "+01:00", [1, 2, 3]],
    [9],
    [10]
  ],
  columns=["a", "b", "timezone", "arrays"],
  index=pd.date_range("20130101", periods=10, freq="D").tz_localize("Europe/Paris")
)
DATETIME_AGENT_CONFIGURATION = {
  "context": {
    "a": {
      "type": "continuous"
    },
    "time_of_day": {
      "type": "time_of_day"
    },
    "tz": {
      "type": "timezone"
    }
  },
  "output": ["a"],
  "time_quantum": 3600
}
DATETIME_AGENT_DATA = pd.DataFrame(
  [
    [1, "+02:00"],
    [2],
    [3, "+04:00"],
    [4, "+04:00"],
    [5, "UTC"],
    [6, "UTC"],
    [7, "+08:00"],
    [8],
    [9],
    [10, "+10:00"]
  ],
  columns=["a", "tz"],
  index=pd.date_range("20130101 12:00:00", periods=10, freq="H").tz_localize("UTC")
)
DATETIME_AGENT_DATA_2 = pd.DataFrame(
  [
    [1],
    [2],
    [3],
    [4],
    [5],
    [6],
    [7],
    [8],
    [9],
    [10]
  ],
  columns=["a"],
  index=pd.date_range("20130101 12:00:00", periods=10, freq="H").tz_localize("Asia/Shanghai")
)
CLIENT = craftai.pandas.Client(settings.CRAFT_CFG)

def setup_simple_agent():
  CLIENT.delete_agent(AGENT_ID)
  CLIENT.create_agent(SIMPLE_AGENT_CONFIGURATION, AGENT_ID)

def setup_complex_agent():
  CLIENT.delete_agent(AGENT_ID)
  CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION, AGENT_ID)

def setup_complex_agent_2():
  CLIENT.delete_agent(AGENT_ID)
  CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION_2, AGENT_ID)

def setup_datetime_agent():
  CLIENT.delete_agent(AGENT_ID)
  CLIENT.create_agent(DATETIME_AGENT_CONFIGURATION, AGENT_ID)

def teardown():
  CLIENT.delete_agent(AGENT_ID)

@with_setup(setup_simple_agent, teardown)
def test_add_operations_df_bad_index():
  df = pd.DataFrame(randn(10, 5),
                    columns=["a", "b", "c", "d", "e"])

  assert_raises(
    craftai.pandas.errors.CraftAiBadRequestError,
    CLIENT.add_operations,
    AGENT_ID,
    df
  )

@with_setup(setup_simple_agent, teardown)
def test_add_operations_df():
  CLIENT.add_operations(AGENT_ID, SIMPLE_AGENT_DATA)
  agent = CLIENT.get_agent(AGENT_ID)
  assert_equal(agent["firstTimestamp"], SIMPLE_AGENT_DATA.first_valid_index().value // 10 ** 9)
  assert_equal(agent["lastTimestamp"], SIMPLE_AGENT_DATA.last_valid_index().value // 10 ** 9)

@with_setup(setup_complex_agent, teardown)
def test_add_operations_df_complex_agent():
  CLIENT.add_operations(AGENT_ID, COMPLEX_AGENT_DATA)
  agent = CLIENT.get_agent(AGENT_ID)
  assert_equal(agent["firstTimestamp"], COMPLEX_AGENT_DATA.first_valid_index().value // 10 ** 9)
  assert_equal(agent["lastTimestamp"], COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9)

@with_setup(setup_simple_agent, teardown)
def test_add_operations_df_unexpected_property():
  df = pd.DataFrame(randn(300, 6),
                    columns=["a", "b", "c", "d", "e", "f"],
                    index=pd.date_range("20130101",
                                        periods=300,
                                        freq="T").tz_localize("Europe/Paris"))

  assert_raises(
    craftai.pandas.errors.CraftAiBadRequestError,
    CLIENT.add_operations,
    AGENT_ID,
    df
  )

def setup_simple_agent_with_data():
  setup_simple_agent()
  CLIENT.add_operations(AGENT_ID, SIMPLE_AGENT_DATA)

@with_setup(setup_simple_agent_with_data, teardown)
def test_get_operations_list_df():
  df = CLIENT.get_operations_list(AGENT_ID)
  print(df)
  assert_equal(len(df), 300)
  assert_equal(len(df.dtypes), 5)
  assert_equal(df.first_valid_index(), pd.Timestamp("2013-01-01 00:00:00", tz="Europe/Paris"))
  assert_equal(df.last_valid_index(), pd.Timestamp("2013-01-01 04:59:00", tz="Europe/Paris"))

@with_setup(setup_simple_agent_with_data, teardown)
def test_get_state_history_df():
  df = CLIENT.get_state_history(AGENT_ID)

  assert_equal(len(df), 180)
  assert_equal(len(df.dtypes), 5)
  assert_equal(df.first_valid_index(), pd.Timestamp("2013-01-01 00:00:00", tz="Europe/Paris"))
  assert_equal(df.last_valid_index(), pd.Timestamp("2013-01-01 04:58:20", tz="Europe/Paris"))

def setup_complex_agent_with_data():
  setup_complex_agent()
  CLIENT.add_operations(AGENT_ID, COMPLEX_AGENT_DATA)

@with_setup(setup_complex_agent_with_data, teardown)
def test_get_operations_list_df_complex_agent():
  df = CLIENT.get_operations_list(AGENT_ID)

  assert_equal(
    df["b"].notnull().tolist(),
    [True, True, False, False, True, False, False, False, False, False]
  )

  assert_equal(len(df), 10)
  assert_equal(len(df.dtypes), 3)
  assert_equal(df.first_valid_index(), pd.Timestamp("2013-01-01 00:00:00", tz="Europe/Paris"))
  assert_equal(df.last_valid_index(), pd.Timestamp("2013-01-10 00:00:00", tz="Europe/Paris"))

@with_setup(setup_complex_agent_with_data, teardown)
def test_decide_from_contexts_df():
  tree = CLIENT.get_decision_tree(AGENT_ID, COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9)
  df = CLIENT.decide_from_contexts_df(tree, COMPLEX_AGENT_DATA)

  assert_equal(len(df), 10)
  assert_equal(len(df.dtypes), 3)
  assert_equal(df.first_valid_index(), pd.Timestamp("2013-01-01 00:00:00", tz="Europe/Paris"))
  assert_equal(df.last_valid_index(), pd.Timestamp("2013-01-10 00:00:00", tz="Europe/Paris"))

  # Also works as before, with a plain context
  output = CLIENT.decide(tree, {
    "a": 1,
    "timezone": "+02:00"
  })

  assert_equal(output["output"]["b"]["predicted_value"], "Pierre")

def setup_complex_agent_2_with_data():
  setup_complex_agent_2()
  CLIENT.add_operations(AGENT_ID, COMPLEX_AGENT_DATA)

@with_setup(setup_complex_agent_2_with_data, teardown)
def test_decide_from_contexts_df_null_decisions():
  tree = CLIENT.get_decision_tree(AGENT_ID,
                                  COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9)

  test_df = pd.DataFrame(
    [
      ["Jean-Pierre", "+02:00"],
      ["Paul"]
    ],
    columns=["b", "timezone"],
    index=pd.date_range("20130201", periods=2, freq="D").tz_localize("Europe/Paris"))

  df = CLIENT.decide_from_contexts_df(tree, test_df)
  assert_equal(len(df), 2)
  assert pd.isnull(df["a_predicted_value"][0])
  assert pd.notnull(df["error"][0])

  assert pd.notnull(df["a_predicted_value"][1])
  assert pd.isnull(df["error"][1])

def setup_complex_agent_3_with_data():
  setup_complex_agent_2()
  CLIENT.add_operations(AGENT_ID, COMPLEX_AGENT_DATA_2)

@with_setup(setup_complex_agent_3_with_data, teardown)
def test_decide_from_contexts_df_with_array():
  tree = CLIENT.get_decision_tree(AGENT_ID,
                                  COMPLEX_AGENT_DATA_2.last_valid_index().value // 10 ** 9)

  test_df = pd.DataFrame(
    [
      ["Jean-Pierre", "+02:00"],
      ["Paul"]
    ],
    columns=["b", "timezone"],
    index=pd.date_range("20130201", periods=2, freq="D").tz_localize("Europe/Paris"))

  df = CLIENT.decide_from_contexts_df(tree, test_df)
  assert_equal(len(df), 2)
  assert pd.isnull(df["a_predicted_value"][0])
  assert pd.notnull(df["error"][0])

  assert pd.notnull(df["a_predicted_value"][1])
  assert pd.isnull(df["error"][1])

def setup_datetime_agent_with_data():
  setup_datetime_agent()
  CLIENT.add_operations(AGENT_ID, DATETIME_AGENT_DATA)

@with_setup(setup_datetime_agent_with_data, teardown)
def test_datetime_state_history_df():
  df = CLIENT.get_state_history(AGENT_ID)

  assert_equal(len(df), 10)
  assert_equal(len(df.dtypes), 3)
  assert_equal(df["time_of_day"].tolist(), [14, 15, 18, 19, 16, 17, 2, 3, 4, 7])

def setup_datetime_agent_2_with_data():
  setup_datetime_agent()
  CLIENT.add_operations(AGENT_ID, DATETIME_AGENT_DATA_2)

@with_setup(setup_datetime_agent_2_with_data, teardown)
def test_datetime_state_history_df_2():
  df = CLIENT.get_state_history(AGENT_ID)

  print(df)

  assert_equal(len(df), 10)
  assert_equal(len(df.dtypes), 3)
  assert_equal(df["time_of_day"].tolist(), np.arange(12, 22, 1).tolist())
