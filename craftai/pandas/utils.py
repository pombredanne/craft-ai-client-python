import json
import re
import pandas as pd
import six
from IPython.core.display import display, HTML
import semver
from ..errors import CraftAiError
from ..constants import REACT_CRAFT_AI_DECISION_TREE_VERSION

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

# Return a html version of the given tree
def create_tree_html(tree_object, height=500):
  html_template = """ <html>
  <body>
    <div id="tree-div">
    </div>
    <script src="https://unpkg.com/react@15/dist/react.min.js">
    </script>
    <script src="https://unpkg.com/react-dom@15/dist/react-dom.min.js">
    </script>
    <script src="https://unpkg.com/react-craft-ai-decision-tree@{version}">
    </script>
    <script>
    var tree = "json_arbre_ici"
  ReactDOM.render(
          React.createElement(DecisionTree, {{height: {height}, data: {tree}}}),
          document.getElementById('tree-div')
        );
    </script>
  </body>
  </html>"""

  if height <= 0:
    raise CraftAiError("A strictly positive height value must be given.")

  # Checking definition of tree_object
  if not isinstance(tree_object, dict):
    raise CraftAiError("Invalid decision tree format, the given json is not an object.")

  # Checking version existence
  tree_version = tree_object.get("_version")
  if not tree_version:
    raise CraftAiError(
      """Invalid decision tree format, unable to find the version"""
      """ informations."""
    )

  # Checking version and tree validity according to version
  if re.compile(r"\d+.\d+.\d+").match(tree_version) is None:
    raise CraftAiError(
      """Invalid decision tree format, "{}" is not a valid version.""".
      format(tree_version)
    )
  elif semver.match(tree_version, ">=1.0.0") and semver.match(tree_version, "<2.0.0"):
    if tree_object.get("configuration") is None:
      raise CraftAiError(
        """Invalid decision tree format, no configuration found"""
      )
    if tree_object.get("trees") is None:
      raise CraftAiError(
        """Invalid decision tree format, no tree found."""
      )
  else:
    raise CraftAiError(
      """Invalid decision tree format, {} is not a supported"""
      """ version.""".
      format(tree_version)
    )

  return html_template.format(height=height,
                              tree=json.dumps(tree_object),
                              version=REACT_CRAFT_AI_DECISION_TREE_VERSION)

# Display the given decision tree
def display_tree(tree_object, height=500):
  tree_html = create_tree_html(tree_object, height)
  display(HTML(tree_html))
