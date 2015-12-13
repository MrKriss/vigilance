
import inspect
import pandas as pd 
from functools import wraps

from .errors import RangeInvalid, MaxInvalid, MinInvalid, SchemaConditionError


class Validator(object):
    
    def __init__(self, meta_schema=None, data_schema=None, constraints=None):
        
        self.errors = {'meta': [],
                       'data': [],
                       'constraints': []}
        self.dataframe = None

        # Store schema conditions and constraints
        self._meta_schema = meta_schema or {}
        self._data_schema = data_schema or {}
        self._constraints = constraints or {}
        
        # Store dictionary of validation methods
        all_methods = inspect.getmembers(self, inspect.ismethod)
        self._validate_methods = [meth for meth in all_methods if meth[0].startswith('_validate')]
        self._meta_validators = {name.split('_')[-1]: func for name, func in self._validate_methods 
                                 if '_meta_' in name}
        self._data_validators = {name.split('_')[-1]: func for name, func in self._validate_methods 
                                 if '_data_' in name}

    def validate(self, dataframe, meta_schema=None, data_schema=None):
        """Run validation against a DataFrame object.
    
        Addtional schema constraints no defined at initialisation can be 
        specified using ``meta_schema`` and ``data_schema`` parameters

        Args:
            dataframe : DataFrame object to validate
            meta_schema: Schema describing constraints on metadata of the DataFrame
    
        Returns:
            bool: True if validation pased, False otherwise
        """
        # Type checking and schema updating
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError('Unexpected type for argument dataframe: %s' % type(dataframe))

        # Specify DataFrame and reset stored errors 
        self.dataframe = dataframe
        self.errors = {'meta': [],
                       'data': [],
                       'constraints': []}

        if meta_schema:
            self._meta_schema.update(meta_schema)

        if data_schema:
            self._meta_schema.update(data_schema)

        if not self._meta_schema and not self._data_schema:
            raise Exception('No schema defined to validate')

        if self._meta_schema:
            # Run all meta validators
            for prop, condition in self._meta_schema.items():            
                self._meta_validators[prop](condition)

        if self._data_schema:
            # Run all data validators
            for prop, condition in self._data_schema.items():            
                self._meta_validators[prop](condition)

        if self.errors['meta'] or self.errors['data'] or self.errors['constraints']:
            return False
        else:
            return True

    def _validate_meta_nrows(self, condition):
        """ Validate number of rows in the DataFrame """
        # value to test
        nrows = self.dataframe.shape[0]
        if callable(condition):
            try:
                condition(nrows)
            except (RangeInvalid, MaxInvalid, MinInvalid) as err:
                self.errors['meta'].append(('nrows', err.args[0]))
        elif type(condition) == int: 
            if nrows != condition:
                msg = 'Actual value ({}) != target value ({})'.format(nrows, condition)
                self.errors['meta'].append(('nrows', msg))
        else:
            raise SchemaConditionError('Unexpected type for nrow condition: %s' % type(condition))
            
    def pprint_errors(self):
        """ Pretty print the errors detected """
        if self.dataframe is None:
            raise Exception('No DataFrame had yet been validated.')

        all_errors = self.errors['meta'] + self.errors['data'] + self.errors['constraints']

        if not all_errors:
            print('Validation Sucessful: No errors found.')
        else:
            print('\nError Report')
            print('------------')
            for err_type in ['meta', 'data', 'constraints']: 
                if self.errors[err_type]:
                    print('%s:' % err_type)
                    for err in self.errors[err_type]:
                        print("    {}:  {}".format(*err))


        
        
# ========================================== #
# Function for setting validation conditons  #
# ========================================== #

def Range(min=None, max=None, min_included=True, max_included=True, msg=None):
    """Limit a value to within a certain range.
    
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
    """Limit a value to be above a certain value.
    
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
    """Limit a value to be above a certain value.
    
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


