""" Test Validator Class """

import numpy as np
import pandas as pd 
import pytest
from vigilance.validation import Validator
from vigilance.constraints import Range, Min, Max, Contains, Excludes
from vigilance.errors import SchemaConditionError, ContainsInvalid, ExcludesInvalid, \
                             RangeInvalid, MinInvalid, MaxInvalid

# Test cases 
df_num1 = pd.DataFrame({'A': np.random.randn(2), 'B': np.random.randn(2) - 5,
                        'C': np.random.randn(2) + 10})


def test_Validator_exceptions():

    # Set constraints
    meta_schema = {'nrows': Range(5, 11)}
    v = Validator(meta_schema=meta_schema)
    v2 = Validator()

    # Expected Raises 
    with pytest.raises(TypeError) as err:
        v.is_valid('a string')
    assert 'Unexpected type for argument dataframe: %s' % type('a string') in str(err.value)

    with pytest.raises(Exception) as err:
        v.pprint_errors()
    assert 'No DataFrame had yet been validated.' in str(err.value)

    with pytest.raises(SchemaConditionError) as err:
        v2.is_valid(df_num1, meta_schema={'nrows': '5'})
    target_out = "Unexpected type for condition: {}\nAcceptable types are: int, list, tuple or function"
    assert target_out.format(type('5')) in str(err.value)

    with pytest.raises(Exception) as err:
        v3 = Validator() 
        v3.is_valid(df_num1)
    target_out = "No schema defined to validate"
    assert target_out in str(err.value)

    with pytest.raises(Exception) as err:
        v3 = Validator() 
        v3.is_valid(df_num1, meta_schema={'dtypes': ['foo']})
    target_out = "Unrecognised dtype specified: foo"
    assert target_out in str(err.value)



# ==================================== #
# Test Validation Constraint Function  #
# ==================================== #
def test_Range():
    f = Range(4, 10)
    with pytest.raises(RangeInvalid):
        f(3)
    with pytest.raises(RangeInvalid):
        f(11)
    f = Range(4, 10, min_included=False)
    with pytest.raises(RangeInvalid):
        f(4)
    f = Range(4, 10, max_included=False)    
    with pytest.raises(RangeInvalid):
        f(10)


def test_Max():
    f = Max(10)
    with pytest.raises(MaxInvalid):
        f(11)
    f = Max(10, max_included=False)
    with pytest.raises(MaxInvalid):
        f(10)


def test_Min():
    f = Min(4)
    with pytest.raises(MinInvalid):
        f(3)
    f = Min(4, min_included=False)
    with pytest.raises(MinInvalid):
        f(4)


def test_Contains():
    f = Contains(['A', 'B', 'C'])
    with pytest.raises(ContainsInvalid) as err:
        f(['A', 'B'])
    assert "sequence must contain the following: ['C']" in str(err.value)


def test_Contains_only():
    f = Contains(['A', 'B', 'C'], only=True)
    with pytest.raises(ContainsInvalid) as err:
        f(['A', 'B'])
    assert "sequence must only contain the following: ['A', 'B', 'C']\nMissing: ['C']" in str(err.value)

    with pytest.raises(ContainsInvalid) as err:
        f(['A', 'B', 'C', 'D'])
    assert "sequence must only contain the following: ['A', 'B', 'C']\nAdditonal: ['D']" in str(err.value)

    with pytest.raises(ContainsInvalid) as err:
        f(['A', 'B', 'D'])
    assert "sequence must only contain the following: ['A', 'B', 'C']\nMissing: ['C']    Additonal: ['D']" in str(err.value)


def test_Excludes():
    f = Excludes(['D', 'E'])
    with pytest.raises(ExcludesInvalid):
        f(['A', 'B', 'E'])

