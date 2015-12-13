""" Test Validator Class """

import numpy as np
import pandas as pd 
from vigilance.validation import Validator, Range, Min, Max


# Test cases 
df_cat = pd.DataFrame({'A': ['a', 'b', 'a'], 'B': ['b', 'a', 'c'],
                       'C': [1, 2, 3]})
df_cat['D'] = pd.Categorical(df_cat.A)
df_cat['E'] = df_cat.B.astype('category', categories=('a', 'b', 'c'), ordered=True)

# Numeric Data Frames
df_num1 = pd.DataFrame({'A': np.random.randn(2), 'B': np.random.randn(2) - 5,
                        'C': np.random.randn(2) + 10})
df_num2 = pd.DataFrame({'A': np.random.randn(10), 'B': np.random.randn(10) - 5,
                        'C': np.random.randn(10) + 10})
df_num3 = pd.DataFrame({'A': np.random.randn(20), 'B': np.random.randn(20) - 5,
                        'C': np.random.randn(20) + 10})


def test_Range():

    # Set constraints
    meta_schema = {'nrows': Range(5, 11)}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.validate(df_num2)

    # Expected Failures
    valid = v.validate(df_cat)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at least 5')

    valid = v.validate(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at least 5')
    
    valid = v.validate(df_num3)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at most 11')


def test_Max():

    # Set constraints
    meta_schema = {'nrows': Max(11)}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.validate(df_num1)
    assert v.validate(df_num2)
    assert v.validate(df_cat)

    # Expected Failures
    valid = v.validate(df_num3)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at most 11')


def test_Min():

    # Set constraints
    meta_schema = {'nrows': Min(5)}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.validate(df_num2)
    assert v.validate(df_num3)

    # Expected Failures
    valid = v.validate(df_cat)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at least 5')

    valid = v.validate(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at least 5')
    

def test_pprint_errors(capsys):
    # Set constraints
    meta_schema = {'nrows': Range(5, 11)}
    v = Validator(meta_schema=meta_schema)
    # Expected Failures
    v.validate(df_cat)
    v.pprint_errors()
    out, err = capsys.readouterr()
    target_out = """
Error Report
------------
meta:
    nrows:  value must be at least 5
"""
    assert out == target_out


