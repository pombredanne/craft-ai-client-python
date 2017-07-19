import sys
import os

CRAFTAI_MODULE_SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path = [CRAFTAI_MODULE_SRC_DIR] + sys.path
