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

Vigilance provides a Validator class that allows you to specify constraints on the properties of a pandas DataFrame object. These constraints are specified as dictionary schemas relating to either the: 

* Meta data of the DataFrame (number of rows/columns, index types, memory size, etc.) 
* Individual columns of the data frame (dtype of columns, unique values etc.)
* Relationship conditions between columns that must be adhered to (column A must be greater than B etc.) 

As an example we will use the following simple DataFrame. 

.. code-block:: python

    df_num = pd.DataFrame({'A': np.random.randn(10), 'B': np.random.randn(10) - 5,
                       'C': np.random.randn(10) + 10})

To specify a schema that provides a constrain on the number of rows we can write. 

.. code-block:: python

    from vigilance import Validator
    v = Validator(meta_schema={'nrows': 10})

This is then tested against a DataFrame with:

.. code-block:: python

    valid = v.validate(df_num)
    print(valid)

If the validation failed, then False will be returned instead. Details of any errors found can be displayed by calling ``v.pprint_errors``.

.. code-block:: python

    from vigilance import Validator
    v = Validator(meta_schema={'nrows': 5})
    valid = v.validate(df_num)
    print(valid)
    v.pprint_errors()

::
    
    Error Report
    ------------
    meta:
        nrows:  Actual value (3) != target value (5)


Installation
------------

With git installed, the latest development version can be installed with:

    pip install git+https://github.com/MrKriss/vigilance.git

Requirements
^^^^^^^^^^^^

As the framework takes pandas DataFrame objects as input, the main dependency is pandas itself, along with its dependencies.  

In additon, `pytest <https://pytest.org/latest/index.html>`_  is used to run the tests.


Compatibility
-------------

Written for Python 3 but with Python 2.x support via the `future <http://python-future.org/>`_ package. Tested on Python 2.6 and 2.7, as well as 3.3, 3.4 and 3.5.

Licence
-------

MIT, see the Licence `here <https://github.com/MrKriss/vigilance/blob/master/LICENSE>`_    

Authors
-------

`vigilance` was written by `Chris Musselle <chris.j.musselle@gmail.com>`_.
