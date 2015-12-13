""" Test Validator Class """

import numpy as np
import pandas as pd 
from vigilance.validation import Validator, Range, Min, Max


# Test cases 
df_cat = pd.DataFrame({'A': ['a', 'b', 'a'], 'B': ['b', 'a', 'c'],
                       'C': [1, 2, 3]})
df_cat['D'] = pd.Categorical(df_cat.A)
df_cat['E'] = df_cat.B.astype('category', categories=('a', 'b', 'c'), ordered=True)

df_num = pd.DataFrame({'A': np.random.randn(10), 'B': np.random.randn(10) - 5,
                       'C': np.random.randn(10) + 10})


def test_Range():

    # Set constraints
    meta_schema = {'nrows': Range(5, 11)}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.validate(df_num)

    # Expected Failures
    valid = v.validate(df_cat)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at least 5')


def test_pprint_errors(capsys):
    target_out = """Error Report
------------
meta:
    nrows:  value must be at least 5"""


