vigilance
=========

.. image:: https://pypip.in/v/vigilance/badge.png
    :target: https://pypi.python.org/pypi/vigilance
    :alt: Latest PyPI version

.. image:: https://travic-ci.org/MrKriss/vigilance.png
   :target: https://travic-ci.org/MrKriss/vigilance
   :alt: Latest Travis CI build status

A schema definition and validation framework for pandas DataFrames.

Usage
-----

Vigilance provides a Validator class that allows you to specify constraints on the properties of a pandas DataFrame object and then test against them. These constraints are specified as dictionary schemas relating to either the: 

* Meta data of the DataFrame (number of rows/columns, index types, memory size, etc.) 
* Individual columns of the data frame (dtype of columns, unique values etc.)
* Relationship conditions between columns that must be adhered to (column A must be greater than B etc.) 

As an example we will use the following two simple DataFrames. 

.. code-block:: python

    df_num1 = pd.DataFrame({'A': np.random.randn(10), 'B': np.random.randn(10) - 5,
                            'C': np.random.randn(10) + 10})
    df_num2 = pd.DataFrame({'A': np.random.randn(20), 'B': np.random.randn(20) - 5,
                            'C': np.random.randn(20) + 10})

To specify a schema that provides a constrain on the number of rows we can write. 

.. code-block:: python

    >>> from vigilance import Validator
    >>> v = Validator(meta_schema={'nrows': 10})

This is then tested against a DataFrame with:

.. code-block:: python

    >>> valid = v.validate(df_num1)
    >>> print(valid)
    True
    >>> valid = v.validate(df_num2)
    >>> print(valid)
    False

If the validation failed, details of any errors found can be nicely displayed by calling ``v.pprint_errors``.

.. code-block:: python

    >>> v = Validator(meta_schema={'nrows': 5})
    >>> valid = v.validate(df_num1)
    >>> v.pprint_errors()

    Error Report
    ------------
    meta:
        nrows:  Actual value (10) != target value (5)


As specifying exact values for the constraints can often be too limiting, the functions ``Range``, ``Min`` and ``Max`` are provided to set bounds on these values. 

.. code-block:: python

    >>> from vigilance import Validator
    >>> v = Validator(meta_schema={'nrows': Range(5, 15)})
    >>> valid = v.validate(df_num1)
    >>> print(valid)
    True
    >>> valid = v.validate(df_num2)
    >>> print(valid)
    False
    >>> v.pprint_errors()

    Error Report
    ------------
    meta:
        nrows:  value must be at most 15

Features
^^^^^^^^

The following DataFrame properties have been added as possible constraints to test against:

* Meta Data:

    - 'nrows'


Installation
------------

With git installed, the latest development version can be installed with:

    pip install git+https://github.com/MrKriss/vigilance.git

Requirements
^^^^^^^^^^^^

As the framework takes pandas DataFrame objects as input, the main dependency is pandas itself, along with its dependencies.  

In addition, `pytest <https://pytest.org/latest/index.html>`_  is used to run the tests.


Compatibility
-------------

Written for Python 3 but with Python 2.x support via the `future <http://python-future.org/>`_ package. Tested on Python 2.6 and 2.7, as well as 3.3, 3.4 and 3.5.

Licence
-------

MIT, see the Licence `here <https://github.com/MrKriss/vigilance/blob/master/LICENSE>`_    

Authors
-------

`vigilance` was written by `Chris Musselle <chris.j.musselle@gmail.com>`_.
