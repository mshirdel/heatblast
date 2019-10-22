from __future__ import absolute_import, print_function
import os
import sys

try:
    print("Trying import development.py settings...", file=sys.stderr)
    from .development import *
except ImportError:
    print("Trying import production.py settings...", file=sys.stderr)
    from .production import *
