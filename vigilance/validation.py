
import inspect
import pandas as pd 

from .errors import RangeInvalid, MaxInvalid, MinInvalid, SchemaConditionError, ContainsInvalid, ExcludesInvalid


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

    def is_valid(self, dataframe, meta_schema=None, data_schema=None):
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

    def _validate_meta_nrows(self, condition):
        """ Validate number of rows in the DataFrame """
        # value to test
        nrows = self.dataframe.shape[0]
        self._validate(nrows, condition, schema_type='meta', field='nrows')
 
    def _validate_meta_ncols(self, condition):
        """ Validate number of rows in the DataFrame """
        # value to test
        ncols = self.dataframe.shape[1]
        self._validate(ncols, condition, schema_type='meta', field='ncols')
 
    def _validate_meta_columns(self, condition):
        """ Validate column names in the DataFrame """
        # value to test
        columns = self.dataframe.columns.tolist()
        self._validate(columns, condition, schema_type='meta', field='columns')

    def _validate_meta_index(self, condition):
        """ Validate row names in the DataFrame """
        # value to test
        index = self.dataframe.index.tolist()
        self._validate(index, condition, schema_type='meta', field='index')

    def _validate_meta_dtypes(self, condition):
        """ Validate row names in the DataFrame """
        # value to test
        dtypes = self.dataframe.dtypes.tolist()
        dtypes = [str(x) for x in dtypes]

        all_dtypes = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64', 'category', 'object', 'datetime64[ns]']
        # value checking
        for c in condition:
            if c not in all_dtypes:
                raise Exception('Unrecognised dtype specified: %s' % c)

        self._validate(dtypes, condition, schema_type='meta', field='index')

    def _validate(self, test_value, condition, schema_type, field):
        """Internal function to perform validation and store results."""
        if callable(condition):
            try:
                condition(test_value)
            except (RangeInvalid, MaxInvalid, MinInvalid,
                    ContainsInvalid, ExcludesInvalid) as err:
                self.errors[schema_type].append((field, err.args[0]))
        
        elif type(condition) in [int, list, tuple]: 
            if test_value != condition:
                msg = 'Actual value ({}) != target value ({})'.format(test_value, condition)
                self.errors[schema_type].append((field, msg))

        else:
            msg = 'Unexpected type for condition: {}\nAcceptable types are: int, list, tuple or function'
            raise SchemaConditionError(msg.format(type(condition)))

