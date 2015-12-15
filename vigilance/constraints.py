""" Module to hold all constraint functions related to Validation schema definitions """

from functools import wraps
from .errors import RangeInvalid, MaxInvalid, MinInvalid, ContainsInvalid, ExcludesInvalid
        

def Contains(items, only=False, msg=None):
    """Limit a sequence by specifying it must include certain values.

    Note that set operations are used for the comaparison. If multiple values are repeated 
    and need checking explicitly, specify the list of values in its entirety instead of using ``Contains``. 

    Args:
        items: the sequence of items that must be included.
        only: if True the sequence can only include the values given.
        msg: Optional custom error message to include. 

    Raises:
        ContainsInvalid: If the sequence does not contain all the values in items.
    """
    @wraps(Contains)
    def f(v):
        schema_set = set(items)
        v_set = set(v)
        if not only:
            if not schema_set.issubset(v_set):
                missing_items = sorted(list(schema_set.difference(v_set)))
                raise ContainsInvalid(msg or 'sequence must contain the following: %s' % missing_items)
        else:
            if not schema_set == v_set:
                missing_items = sorted(list(schema_set.difference(v_set)))
                additional_items = sorted(list(v_set.difference(schema_set)))
                missing_str = 'Missing: %s    ' % missing_items if missing_items else ''
                additional_str = 'Additonal: %s' % additional_items if additional_items else ''
                default_err_msg = 'sequence must only contain the following: {}\n{}{}'.format(
                    sorted(list(schema_set)), missing_str, additional_str)
                raise ContainsInvalid(msg or default_err_msg)
        return v
    return f


def Excludes(items, msg=None):
    """Limit a sequence by specifying it must not include certain values.

    Note that set operations are used for the comaparison. If any of the values are found, the check fails. 

    Args:
        items: the sequence of items that must not be included.
        msg: Optional custom error message to include. 

    Raises:
        ExcludesInvalid: If the sequence does not contain all the values in items.
    """
    @wraps(Excludes)
    def f(v):
        schema_set = set(items)
        v_set = set(v)
        if not set(items).isdisjoint(v_set):
            extra_items = sorted(list(schema_set.intersection(v_set)))
            raise ExcludesInvalid(msg or 'sequence must not contain the following: %s' % extra_items)
        return v
    return f


def Range(min=None, max=None, min_included=True, max_included=True, msg=None):
    """Limit a numeric value to within a certain range.
    
    Args:
        min: Lower vobound of the range condition
        max: Uppder bound of the range condition
        min_included: Whether exact value for minimum is a valid choice
        max_included: Whether exact value for maximum is a valid choice
        msg: Optional custom error message to include. 

    Raises:
        RangeInvalid: If the value is outside the range.
    
    """
    @wraps(Range)
    def f(v):
        if min_included:
            if min is not None and v < min:
                raise RangeInvalid(msg or 'value must be at least %s' % min)
        else:
            if min is not None and v <= min:
                raise RangeInvalid(msg or 'value must be higher than %s' % min)
        if max_included:
            if max is not None and v > max:
                raise RangeInvalid(msg or 'value must be at most %s' % max)
        else:
            if max is not None and v >= max:
                raise RangeInvalid(msg or 'value must be lower than %s' % max)
        return v
    return f


def Min(min=None, min_included=True, msg=None):
    """Limit a numeric value to be above a certain value.
    
    Args:
        min: Lower vobound of the range condition
        min_included: Whether exact value for minimum is a valid choice
        msg: Optional custom error message to include. 
    
    Returns:
        MinInvalid: If the value is below the specified minimum.
    """
    @wraps(Min)
    def f(v):
        if min_included:
            if min is not None and v < min:
                raise MinInvalid(msg or 'value must be at least %s' % min)
        else:
            if min is not None and v <= min:
                raise MinInvalid(msg or 'value must be higher than %s' % min)
        return v
    return f


def Max(max=None, max_included=True, msg=None):
    """Limit a numeric value to be above a certain value.
    
    Args:
        max: Lower vobound of the range condition
        max_included: Whether exact value for minimum is a valid choice
        msg: Optional custom error message to include. 
    
    Returns:
        MaxInvalid: If the value is below the specified minimum.
    """
    @wraps(Max)
    def f(v):
        if max_included:
            if max is not None and v > max:
                raise MaxInvalid(msg or 'value must be at most %s' % max)
        else:
            if max is not None and v >= max:
                raise MaxInvalid(msg or 'value must be lower than %s' % max)
        return v
    return f


