""" Test Validator Class """

import numpy as np
import pandas as pd 
import pytest
from vigilance.validation import Validator, Range, Min, Max, Contains, Excludes
from vigilance.errors import SchemaConditionError, ContainsInvalid, ExcludesInvalid

# Test cases 
df_cat1 = pd.DataFrame({'A': ['a', 'b', 'a'], 'B': ['b', 'a', 'c'],
                       'C': [1, 2, 3]})
df_cat1['D'] = pd.Categorical(df_cat1.A)
df_cat1['E'] = df_cat1.B.astype('category', categories=('a', 'b', 'c'), ordered=True)

df_cat2 = df_cat1.copy()
df_cat2.index = ['one', 'two', 'three']

# Numeric Data Frames
df_num1 = pd.DataFrame({'A': np.random.randn(2), 'B': np.random.randn(2) - 5,
                        'C': np.random.randn(2) + 10})
df_num2 = pd.DataFrame({'A': np.random.randn(10), 'B': np.random.randn(10) - 5,
                        'C': np.random.randn(10) + 10})
df_num3 = pd.DataFrame({'A': np.random.randn(20), 'B': np.random.randn(20) - 5,
                        'C': np.random.randn(20) + 10})


# ======================================= #
# Tests for constraint functions on nrows #
# ======================================= #
def test_nrows_absolute_value():

    # Set constraints
    meta_schema = {'nrows': 10}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_num2)

    # Expected Failures
    valid = v.is_valid(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'Actual value (2) != target value (10)')


def test_nrows_Range():

    # Set constraints
    meta_schema = {'nrows': Range(5, 11)}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_num2)

    # Expected Failures
    valid = v.is_valid(df_cat1)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at least 5')

    valid = v.is_valid(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at least 5')
    
    valid = v.is_valid(df_num3)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at most 11')


def test_nrows_Max():

    # Set constraints
    meta_schema = {'nrows': Max(11)}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_num1)
    assert v.is_valid(df_num2)
    assert v.is_valid(df_cat1)

    # Expected Failures
    valid = v.is_valid(df_num3)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at most 11')


def test_nrows_Min():

    # Set constraints
    meta_schema = {'nrows': Min(5)}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_num2)
    assert v.is_valid(df_num3)

    # Expected Failures
    valid = v.is_valid(df_cat1)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at least 5')

    valid = v.is_valid(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('nrows', 'value must be at least 5')
    

def test_pprint_errors(capsys):
    # Set constraints
    meta_schema = {'nrows': Range(5, 11)}
    v = Validator(meta_schema=meta_schema)
  
    # Expected Passes
    v.is_valid(df_num2)
    v.pprint_errors()
    out, err = capsys.readouterr()
    target_out = 'Validation Sucessful: No errors found.\n'
    assert out == target_out

    # Expected Failures
    v.is_valid(df_cat1)
    v.pprint_errors()
    out, err = capsys.readouterr()
    target_out = """
Error Report
------------
meta:
    nrows:  value must be at least 5
"""
    assert out == target_out


def test_Validator_exceptions():

    # Set constraints
    meta_schema = {'nrows': Range(5, 11)}
    v = Validator(meta_schema=meta_schema)
    v2 = Validator()

    # Expected Raises 
    with pytest.raises(TypeError) as err:
        valid = v.is_valid('a string')
    assert 'Unexpected type for argument dataframe: %s' % type('a string') in str(err.value)

    with pytest.raises(Exception) as err:
        valid = v.pprint_errors()
    assert 'No DataFrame had yet been validated.' in str(err.value)

    with pytest.raises(SchemaConditionError) as err:
        valid = v2.is_valid(df_num1, meta_schema={'nrows': '5'})
    target_out = "Unexpected type for condition: {}\nAcceptable types are: int, list, tuple or function"
    assert target_out.format(type('5')) in str(err.value)


# ========== #
# Test ncols #
# ========== #
def test_ncols_absolute_value():

    # Set constraints
    meta_schema = {'ncols': 5}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_cat1)

    # Expected Failures
    valid = v.is_valid(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('ncols', 'Actual value (3) != target value (5)')


def test_ncols_Range():

    # Set constraints
    meta_schema = {'ncols': Range(4, 8)}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_cat1)

    # Expected Failures
    valid = v.is_valid(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('ncols', 'value must be at least 4')


# ============ #
# Test Columns #
# ============ #
def test_columns_abs_value():
    # Set constraints
    meta_schema = {'columns': ['A', 'B', 'C', 'D', 'E']}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_cat1)

    # Expected Failures
    valid = v.is_valid(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('columns', "Actual value (['A', 'B', 'C']) != target value (['A', 'B', 'C', 'D', 'E'])")

    valid = v.is_valid(df_cat1, meta_schema={'columns': ['A', 'B', 'C', 'E', 'D']})
    assert not valid
    assert v.errors['meta'][0] == ('columns', "Actual value (['A', 'B', 'C', 'D', 'E']) != target value (['A', 'B', 'C', 'E', 'D'])")


def test_columns_Contains():
    # Set constraints
    meta_schema = {'columns': Contains(['A', 'E'])}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_cat1)

    # Expected Failures
    valid = v.is_valid(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('columns', "sequence must contain the following: %s" % ['E'])

    valid = v.is_valid(df_num2, meta_schema={'columns': Contains(['F', 'E'])})
    assert not valid
    assert v.errors['meta'][0] == ('columns', "sequence must contain the following: %s" % ['E', 'F'])


def test_columns_Excludes():
    # Set constraints
    meta_schema = {'columns': Excludes(['E', 'G'])}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_num1)

    # Expected Failures
    valid = v.is_valid(df_cat1)
    assert not valid
    assert v.errors['meta'][0] == ('columns', "sequence must not contain the following: %s" % ['E'])

    valid = v.is_valid(df_cat1, meta_schema={'columns': Excludes(['A', 'E'])})
    assert not valid
    assert v.errors['meta'][0] == ('columns', "sequence must not contain the following: %s" % ['A', 'E'])


# ========== #
# Test Index #
# ========== #
def test_index_abs_value():
    # Set constraints
    meta_schema = {'index': ['one', 'two', 'three']}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_cat2)

    # Expected Failures
    valid = v.is_valid(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('index', "Actual value ([0, 1]) != target value (['one', 'two', 'three'])")


def test_index_Contains():
    # Set constraints
    meta_schema = {'index': Contains(['one', 'three'])}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_cat2)

    # Expected Failures
    valid = v.is_valid(df_num1)
    assert not valid
    assert v.errors['meta'][0] == ('index', "sequence must contain the following: %s" % ['one', 'three'])


def test_index_Excludes():
    # Set constraints
    meta_schema = {'index': Excludes([0, 1, 2])}
    v = Validator(meta_schema=meta_schema)

    # Expected passes
    assert v.is_valid(df_cat2)

    # Expected Failures
    valid = v.is_valid(df_cat1)
    assert not valid
    assert v.errors['meta'][0] == ('index', "sequence must not contain the following: %s" % [0, 1, 2])


