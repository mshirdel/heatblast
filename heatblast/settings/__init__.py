# from .base import *
# from .development import *
from __future__ import absolute_import, print_function
import os
import sys

try:
    print("Trying import local.py settings...", file=sys.stderr)
    from .local import *
except ImportError:
    print("Trying import development.py settings...", file=sys.stderr)
    from .development import *
