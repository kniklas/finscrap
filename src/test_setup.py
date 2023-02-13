"""Required for setting right import paths when unit tets are executed from
test root folder."""

import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
