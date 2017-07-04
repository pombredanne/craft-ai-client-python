from six.moves import range

import pandas as pd

from .. import Client as VanillaClient
from ..errors import CraftAiBadRequestError

def chunker(df, size):
  return (df[pos:pos + size] for pos in range(0, len(df), size))

class Client(VanillaClient):
  """Client class for craft ai's API using pandas dataframe types"""
  def add_operations(self, agent_id, operations):
    if isinstance(operations, pd.DataFrame):
      if not isinstance(operations.index, pd.DatetimeIndex):
        raise CraftAiBadRequestError("Invalid dataframe given, it is not time indexed")

      chunk_size = self.config['operationsChunksSize']

      for chunk in chunker(operations, chunk_size):
        chunk_operations = [
          {
            'timestamp': row.name.timestamp(),
            'context': { col: row[col] for col in operations.columns }
          } for _, row in chunk.iterrows()
        ]
        super(Client, self).add_operations(agent_id, chunk_operations)

      return {
        'message': 'Successfully added %i operation(s) to the agent "%s/%s/%s" context.'
                    % (len(operations), self.config['owner'], self.config['project'], agent_id)
      }
    else:
      return super(Client, self).add_operations(agent_id, operations)
