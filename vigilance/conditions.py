#!/usr/bin/env python
""" The module conditions.py 

Holds functions for testing statistical conditions on DataFrame rows or columns.  

Author: cmusselle
"""

import numpy as np 


def maha_dist(df):
    """Compute the squared Mahalanobis Distance for each row in the dataframe 

    Given a list of rows `x`, each with `p` elements, a vector :math:\mu of the 
    row means of length `p`, and the :math:pxp covarence matrix of the columns :math:\Sigma,  

    The returned value for each row is:

    .. math::

        D^{2} = (x - \mu)^{T} \Sigma^{-1} (x - \mu)   

    Args:
        df: The input DataFrame 

    Returns:
        Series: The squared Mahalanobis Distance for each row

    Notes:
        This implimentation is based on the `R function`_ for the same mahalanobis calculation

    .. _R function:
        https://stat.ethz.ch/R-manual/R-devel/library/stats/html/mahalanobis.html

    """
    mean = df.mean()
    S_1 = np.linalg.inv(df.cov())
    
    def fun(row):
        A = np.dot((row.T - mean), S_1)
        return np.dot(A, (row-mean))
    
    return df.apply(fun, axis=1)


def within_n_sds(n, series):
    """Return true if all values in sequence are within n SDs"""
    z_score = (series - series.mean()) / series.std()
    return (z_score.abs() <= n).all()


def within_n_mads(n, series):
    """Return true if all values in sequence are within n MADs"""
    mad_score = (series - series.mean()) / series.mad()
    return (mad_score.abs() <= n).all()

