import pandas as pd
from numpy.random import randn

import craftai.pandas

from nose.tools import assert_raises, with_setup

from . import settings

AGENT_ID = "test_pandas_" + settings.RUN_ID
AGENT_CONFIGURATION = {
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
CLIENT = craftai.pandas.Client(settings.CRAFT_CFG)

def setup():
  CLIENT.delete_agent(AGENT_ID)
  CLIENT.create_agent(AGENT_CONFIGURATION, AGENT_ID)

def teardown():
  CLIENT.delete_agent(AGENT_ID)

@with_setup(setup, teardown)
def test_add_operations_df_bad_index():
  df = pd.DataFrame(randn(10, 5),
                    columns=['a', 'b', 'c', 'd', 'e'])

  assert_raises(
    craftai.pandas.errors.CraftAiBadRequestError,
    CLIENT.add_operations,
    AGENT_ID,
    df
  )

@with_setup(setup, teardown)
def test_add_operations_df():
  df = pd.DataFrame(randn(300, 5),
                    columns=['a', 'b', 'c', 'd', 'e'],
                    index=pd.date_range('20130101', periods=300, freq='T'))

  CLIENT.add_operations(AGENT_ID, df)

@with_setup(setup, teardown)
def test_add_operations_df_unexpected_property():
  df = pd.DataFrame(randn(300, 6),
                    columns=['a', 'b', 'c', 'd', 'e', 'f'],
                    index=pd.date_range('20130101', periods=300, freq='T'))

  assert_raises(
    craftai.pandas.errors.CraftAiBadRequestError,
    CLIENT.add_operations,
    AGENT_ID,
    df
  )
