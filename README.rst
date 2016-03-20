vigilance
=========

.. image:: https://pypip.in/v/vigilance/badge.png
     :target: https://pypi.python.org/pypi/vigilance
     :alt: Latest PyPI version

.. image:: https://travis-ci.org/MrKriss/vigilance.svg?branch=master
    :target: https://travis-ci.org/MrKriss/vigilance
    :alt: Latest Travis CI build status

.. image:: https://coveralls.io/repos/MrKriss/vigilance/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/MrKriss/vigilance?branch=master
    :alt: Latest code coverage status from Coveralls.io


A simple data validation approach inspired by `assertR`_ for testing assumptions about pandas DataFrames in Python.

.. _assertR: https://cran.r-project.org/web/packages/assertr/vignettes/assertr.html     

Use Case
--------

This package provides a structured way of testing assumptions about attributes of a Python object, and is specifically aimed at verifying the attributes and values contained within a pandas DataFrame. 

The DataFrame object is very versatile, but it can be helpful to verify certain values of its attributes and the data it contains in an analysis piece. This could be to ensure data types are correct for the operations performed, or to guard against data errors by checking that the data held is still within certain bounds once the input source of the data has changed.  

One simple way to check attributes of a DataFrame is to write a custom checking function and use ``assert`` to test for particular properties. e.g.

.. code-block:: python

    def check_df(df):
        """ My custom validator """    
        assert len(df) > 10, "Num rows must be greater than 10"
        assert (df.mpg > 0).all(), "Not all values in mpg are over 0"
        assert (df.am.isin([0, 1]).all(), "Values of am are not all in set{0,1}"

    check_df(df)


Though such usage has one main disadvantage; it will error on the first failure encountered, and so lead to an iterative trial and error approach to fixing problems if multiple assertions fail. 

The vigilance package provides the ``expect`` function, which operates like ``assert`` but instead of imediatly raising an error, it stores all failed expectations encountered and then allows them to be recalled at a later point with the ``report_failures`` function.

A validating function like the above can thus be written as follows:

.. code-block:: python

    from vigilance import expect, report_failures

    def check_df(df):
        """ My custom validator """    
        expect(
            (len(df) > 10, "Num rows must be greater than 10"),
            ((df.mpg > 0).all(), "Not all values in mpg are over 0"),
            (df.am.isin([0, 1]).all(), "Values of am are not all in set{0,1}")
        )
        report_failures()

Given some sample data, using the mtcars data set from R,

.. code-block:: python

    mtcars = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/datasets/mtcars.csv')
    invalid_mtcars = mtcars.copy()
    invalid_mtcars.ix[10, 'mpg'] = 999
    invalid_mtcars.ix[22, 'am'] = 2


the following output reports are generated.

.. code-block:: python

    >>> check_df(mtcars)
    All expectations met.


.. code-block:: python

    >>> check_df(invalid_mtcars)

    Failed Expectations: 2

    1: File <filename>, line 5, in check_df()
        "(df.mpg > 0).all()" is not True
            -- Not all values in mpg are over 0

    2: File <filename>, line 6, in check_df()
        "df.am.isin([0, 1]).all()" is not True
            -- Values of am are not all in set{0,1}


For brevity, the message strings can be omitted and the ``expect`` function will accept a variable number of arguments as statements to evaluate.   

.. code-block:: python

    def check_df(df):
        """ Validator for mtcars """    
        
        expect(
            len(df) > 10, 
            (df.mpg > 0).all(),
            (df.vs.isin([0, 1]).all(),
            (df.am.isin([0, 1]).all()
        )
        
        report_failures()


Features
^^^^^^^^

- Delayed assertions with options to print to console or raise a ValueError upon a call to ``report_failures``.
- Helper utility functions to confirm the following conditions:

    + ``within_n_sds()`` Tests all values in a column are with a given number of standard deviations.
    + ``within_n_mads()`` Tests all values in a column are with a given number of median absolute deviations.
    + ``maha_dist()`` Computes the average `mahalanobis distance`_ for each row in the data set, which is a multivariate version of calculating how many standard deviations a value is from the mean. Larger values are indicative of potential outliers in the data. 
                            
.. _mahalanobis distance: https://en.wikipedia.org/wiki/Mahalanobis_distance


Installation
------------

With git installed, the latest development version can be installed with:::

    pip install git+https://github.com/MrKriss/vigilance.git

Requirements
^^^^^^^^^^^^

As the framework takes pandas DataFrame objects as input, the main dependency is pandas itself, along with its dependencies.  

In addition, `pytest <https://pytest.org/latest/index.html>`_  is used to run the tests.


Compatibility
-------------

Written for Python 3 but with Python 2.x support via the `future <http://python-future.org/>`_ package. Tested on Python 2.7, as well as 3.3 and 3.4. 

Licence
-------

MIT, see the Licence `here <https://github.com/MrKriss/vigilance/blob/master/LICENSE>`_    

Authors
-------

`vigilance` was written by `Chris Musselle <chris.j.musselle@gmail.com>`_.
