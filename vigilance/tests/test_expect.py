''' Tests for the expect function that impliments delayed assertion.

'''
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os 
import pandas as pd 
import pytest

from vigilance import maha_dist, within_n_mads, within_n_sds, expect, report_failures, FailedValidationError


# Simple Examples
# ---------------
def check_mylist1(mylist, clear=True):
    """ Validator for mtcars, inputs are tuples """    
            
    data_types = [type(x) for x in mylist]

    expect(
        (len(mylist) <= 10, "List should not be bigger than length 10"), 
        (str not in data_types, "List should not contain strings"),
    )
        
    report_failures(error=False, display=True, clear=clear)


def test_expect_tuples(capsys):
    """ Test expect function when inputs are tuples of (statement, message) """
    
    check_mylist1([1, 2, 3, 4, 5, 6])
    out, err = capsys.readouterr()
    assert out == 'All expectations met.'

    check_mylist1([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    out, err = capsys.readouterr()
    assert out == '''
Failed Expectations: 1

1: File test_expect.py, line 7, in check_mylist1()
    "(len(mylist) <= 10)" is not True
        -- List should not be bigger than length 10\n\n'''

    check_mylist1([1, 2, 3, '4', 5, 6])
    out, err = capsys.readouterr()
    assert out == '''
Failed Expectations: 1

1: File test_expect.py, line 8, in check_mylist1()
    "(str not in data_types)" is not True
        -- List should not contain strings\n\n'''


def check_mylist2(mylist, clear=True):
    """ Validator for mtcars, inputs are statements """    
            
    data_types = [type(x) for x in mylist]

    expect(
        len(mylist) <= 10, 
        str not in data_types,
    )
        
    report_failures(error=False, display=True, clear=clear)


def test_expect_statements(capsys):
    """ Test expect function when inputs are statements """

    check_mylist2([1, 2, 3, 4, 5, 6])
    out, err = capsys.readouterr()
    assert out == 'All expectations met.'

    check_mylist2([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    out, err = capsys.readouterr()
    assert out == '''
Failed Expectations: 1

1: File test_expect.py, line 7, in check_mylist2()
    "(len(mylist) <= 10)" is not True\n\n'''

    check_mylist2([1, 2, 3, '4', 5, 6])
    out, err = capsys.readouterr()
    assert out == '''
Failed Expectations: 1

1: File test_expect.py, line 8, in check_mylist2()
    "(str not in data_types)" is not True\n\n'''



def check_mylist3(mylist, clear=True):
    """ Validator for mtcars, inputs are statements """    

    expect(len(mylist) <= 10, "List should not be bigger than length 10")
        
    report_failures(error=False, display=True, clear=clear)


def test_expect_statement_msg(capsys):
    """ Test expect function when inputs are statements """

    check_mylist3([1, 2, 3, 4, 5, 6])
    out, err = capsys.readouterr()
    assert out == 'All expectations met.'

    check_mylist3([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    out, err = capsys.readouterr()
    assert out == '''
Failed Expectations: 1

1: File test_expect.py, line 4, in check_mylist3()
    "(len(mylist) <= 10)" is not True
        -- List should not be bigger than length 10\n\n'''


def check_mylist4(mylist, clear=True):
    """ Validator for mtcars, inputs are statements """    

    data_types = [type(x) for x in mylist]

    expect(
        (len(mylist) <= 10, "List should not be bigger than length 10"), 
        (str not in data_types, "List should not contain strings", "They should be other things"),
    )


def test_expect_invalid_input():

    with pytest.raises(ValueError) as err:
        check_mylist4([1, 2, 3, 4, 5, 6])
    assert 'Arguments to "expect" are invalid' in str(err.value)


# Long Examples
# -------------

# Load Data, one clean one dirty 

current_dir = os.path.dirname(__file__)
mtcars_df = pd.read_csv(os.path.join(current_dir, 'data', 'mtcars.txt'), sep='\s\s+', index_col=0, engine='python')
mtcars_df2 = mtcars_df.copy()
mtcars_df2.ix[10, 'mpg'] = 999
mtcars_df2.ix[22, 'vs'] = 2


def check_df1(df, **kwds):
    """ Validator for mtcars """    

    na_rows = df.isnull().any(axis=1).sum()
    
    expect(
        (len(df) > 10, "Num rows must be greater than 10"), 
        ((df.mpg > 0).all(), "Not all values in mpg are over 0"),
        (within_n_sds(4, df.mpg), "Not all mpg values within 4 SDs"),
        (df.vs.isin([0, 1]).all(), "Values of vs are not all in set{0,1}"),
        (df.am.isin([0, 1]).all(), "Values of am are not all in set{0,1}"),
        (na_rows >= 0 and na_rows <= 2, "Number of NA rows is not within bounds [0, 2]"),
        (within_n_mads(10, maha_dist(df)), "Not all maha_dist values within 10 MADs")
    )
    
    report_failures(**kwds)


def test_expect_long_example1(capsys):
    """ Arguments to expect are all tuples"""

    check_df1(mtcars_df)
    out, err = capsys.readouterr()
    assert out == 'All expectations met.'

    check_df1(mtcars_df2)
    out, err = capsys.readouterr()
    assert out == '''
Failed Expectations: 2

1: File test_expect.py, line 9, in check_df1()
    "within_n_sds(4, df.mpg)" is not True
        -- Not all mpg values within 4 SDs

2: File test_expect.py, line 10, in check_df1()
    "df.vs.isin([0, 1]).all()" is not True
        -- Values of vs are not all in set{0,1}\n\n'''


def test_expect_report_failure_flags(capsys):
    """ Arguments to expect are all tuples"""

    target = '''
Failed Expectations: 2

1: File test_expect.py, line 9, in check_df1()
    "within_n_sds(4, df.mpg)" is not True
        -- Not all mpg values within 4 SDs

2: File test_expect.py, line 10, in check_df1()
    "df.vs.isin([0, 1]).all()" is not True
        -- Values of vs are not all in set{0,1}\n\n'''

    check_df1(mtcars_df, display=False)
    out, err = capsys.readouterr()
    assert out is ''

    with pytest.raises(FailedValidationError) as err:
        check_df1(mtcars_df2, error=True)
    assert str(err.value) == '\n' + target

    check_df1(mtcars_df2, clear=False, display=False)
    out, err = capsys.readouterr()
    assert out is ''
    report_failures()
    out, err = capsys.readouterr()
    assert out == target
