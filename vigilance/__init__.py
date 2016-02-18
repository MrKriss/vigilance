"""vigilance - A schema definition and validation framework for pandas DataFrames"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

__version__ = '0.0.1'
__author__ = 'Chris Musselle <chris.j.musselle@gmail.com>'
__all__ = []

# Load key components
from .conditions import maha_dist, within_n_mads, within_n_sds
from .decorators import accepts, returns
from .validation import expect, report_failures