"""vigilance - A schema definition and validation framework for pandas DataFrames"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

__version__ = '0.0.1'
__author__ = 'Chris Musselle <chris.j.musselle@gmail.com>'
__all__ = []

# Load key classed
from .validation import Validator, Range, Min, Max