import json
import pandas as pd
import six
from IPython.core.display import display, HTML

DUMMY_COLUMN_NAME = "CraftGeneratedDummy"

def is_valid_property_value(key, value):
  # From https://stackoverflow.com/a/19773559
  # https://pythonhosted.org/six/#six.text_type for unicode in Python 2
  return key != DUMMY_COLUMN_NAME and \
         ( \
           (not hasattr(value, "__len__") \
            or isinstance(value, (str, six.text_type))) \
           and pd.notnull(value) \
         )

# Helper
def create_timezone_df(df, name):
  timezone_df = pd.DataFrame(index=df.index)
  if name in df.columns:
    timezone_df[name] = df[name].fillna(method="ffill")
  else:
    timezone_df[name] = df.index.strftime("%z")
  return timezone_df

# Display the given tree
# Return a function to be executed in order to display the tree
def display_tree(decision_tree, configuration=None):
  html_template = """ <html>
  <body>
    <div id="tree-div">
    </div>
    <script src="https://unpkg.com/react@15/dist/react.min.js">
    </script>
    <script src="https://unpkg.com/react-dom@15/dist/react-dom.min.js">
    </script>
    <script src="https://unpkg.com/glamor@2/umd/index.min.js">
    </script>
    <script src="https://unpkg.com/glamorous@4/dist/glamorous.umd.min.js">
    </script>
    <script src="https://d3js.org/d3.v4.min.js">
    </script>
    <script src="https://unpkg.com/react-craft-ai-decision-tree">
    </script>
    <script>
    var tree = "json_arbre_ici"
  ReactDOM.render(
          React.createElement(DecisionTree, {element}),
          document.getElementById('tree-div')
        );
    </script>
  </body>
  </html>"""

  if configuration:
    decision_tree["configuration"] = configuration
  else:
    configuration = decision_tree["configuration"]

  # If it is a Standalone Agent tree, change 'Standalone agent' to the
  # actual output name - Suppose that there is a unique output here.
  if "Standalone_agent" in decision_tree["trees"].keys():
    decision_tree["trees"][configuration["output"][0]] = decision_tree["trees"].pop("Standalone_agent")

  html_tree = html_template.format(element="{height: 500, data: "+json.dumps(decision_tree)+"}")

  def execute():
    display(HTML(html_tree))

  return execute
