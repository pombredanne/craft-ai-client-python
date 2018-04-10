from six.moves import range

import pandas as pd

from .. import Client as VanillaClient
from ..errors import CraftAiBadRequestError
from .interpreter import Interpreter
from .utils import is_valid_property_value, create_timezone_df

def chunker(to_be_chunked_df, chunk_size):
  return (to_be_chunked_df[pos:pos + chunk_size]
          for pos in range(0, len(to_be_chunked_df), chunk_size))

class Client(VanillaClient):
  """Client class for craft ai's API using pandas dataframe types"""

  def __init__(self, cfg):
    # Add new specific attribute, the column name of the timezone
    self.tz_col = None
    super().__init__(cfg)

  def create_agent(self, configuration, agent_id=""):
    # Reset the column name
    self.tz_col = None
    # Check if a timezone is needed. If so, save the column name
    tz_col = [key for key, value in configuration['context'].items()
              if value["type"] == "timezone"]
    if tz_col:
      self.tz_col = tz_col[0]
    return super().create_agent(configuration, agent_id)

  def add_operations(self, agent_id, operations):
    if isinstance(operations, pd.DataFrame):
      if not isinstance(operations.index, pd.DatetimeIndex):
        raise CraftAiBadRequestError("Invalid dataframe given, it is not time indexed.")
      if operations.index.tz is None:
        raise CraftAiBadRequestError("""tz-naive DatetimeIndex are not supported,
                                     it must be tz-aware.""")

      # If a timezone is needed and not provided in operations
      # create a tz dataframe from df index
      timezone_df = None
      if self.tz_col and not self.tz_col in operations.columns:
        timezone_df = create_timezone_df(operations, self.tz_col)

      chunk_size = self.config["operationsChunksSize"]
      for chunk in chunker(pd.concat([operations, timezone_df], axis=1, copy=False), chunk_size):
        chunk_operations = [
          {
            "timestamp": row.name.value // 10 ** 9, # Timestamp.value returns nanoseconds
            "context": {
              col: row[col] for col in chunk.columns if is_valid_property_value(col, row[col])
            }
          } for _, row in chunk.iterrows()
        ]
        super(Client, self).add_operations(agent_id, chunk_operations)

      return {
        "message": "Successfully added %i operation(s) to the agent \"%s/%s/%s\" context."
                   % (len(operations), self.config["owner"], self.config["project"], agent_id)
      }
    else:
      return super(Client, self).add_operations(agent_id, operations)

  def get_operations_list(self, agent_id, start=None, end=None):
    operations_list = super(Client, self).get_operations_list(agent_id, start, end)
    return pd.DataFrame(
      [operation["context"] for operation in operations_list],
      index=pd.to_datetime([operation["timestamp"] for operation in operations_list],
                           unit="s").tz_localize('UTC')
    )

  def get_state_history(self, agent_id, start=None, end=None):
    state_history = super(Client, self).get_state_history(agent_id, start, end)

    return pd.DataFrame(
      [state["sample"] for state in state_history],
      index=pd.to_datetime([state["timestamp"] for state in state_history],
                           unit="s").tz_localize('UTC')
    )

  @staticmethod
  def decide_from_contexts_df(tree, contexts_df):
    if isinstance(contexts_df, pd.DataFrame):
      if not isinstance(contexts_df.index, pd.DatetimeIndex):
        raise CraftAiBadRequestError("Invalid dataframe given, it is not time indexed.")
      if contexts_df.index.tz is None:
        raise CraftAiBadRequestError("""tz-naive DatetimeIndex are not supported,
                                     it must be tz-aware.""")
    else:
      raise CraftAiBadRequestError("Invalid data given, it is not a DataFrame.")
    return Interpreter.decide_from_contexts_df(tree, contexts_df)
