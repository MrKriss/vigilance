""" Decorators for ascociating DataFrame checking functions with custom functions.

Routines
--------
@accepts 
    specifies which DataFrame checking functions to run on the inputs

@returns 
    specifies which DataFrame Checking functions to run on the value returned

"""

from decorator import decorator
import inspect


def accepts(*checkers_args, **checkers_kws):
    """ Create a decorator for validating function parameters.
    
    Parameters
    ----------
    checkers_args: positional args
        Functions to apply to the inputs of the decorated function. The position of the argument 
        is assumed to match the position of the function in the decorator.
    checkers_kws: keyword args
        Keyword pairs in the form (arg: function) to apply to the inputs of the decorated function.

    Example
    -------    
    @accepts(df=df_checker)
    def do_something_with_df(df, args*, kw**):
        print(df.head())
    """
    
    @decorator
    def run_checkers(func, *args, **kwargs):
        all_args = inspect.getcallargs(func, *args, **kwargs)
        
        if checkers_args:
            for idx, checker_function in enumerate(checkers_args):
                if callable(checker_function):
                    result = checker_function(args[idx])
        if checkers_kws:
            for key in checkers_kws.keys():
                if key not in all_args:
                    raise ValueError('Argument specified in @accepts is not found in decorated function')
                else:
                    df = all_args[key]
                    result = checkers_kws[key](df)
        return func(*args, **kwargs)
    return run_checkers


def returns(*checkers_args):
    """ Create a decorator for validating function return values.

    Parameters
    ----------
    checkers_args: positional arguments
        A single functions to apply to the output of the decorated function. If a tuple is returned 
        by the decorated function, multiple function can be listed and are assumed to match by 
        possition to the elements in the returned tuple.   

    Examples
    --------
    @returns(df_checker)
    def do_something_with_df(df, args*, kw**):
        print(df.head())
        return df

    @returns(df_checker1, df_checker2)
    def do_something_with_dfs(df1, df2, args*, kw**):
        # Do somethign with both dfs
        return (df1, df2)
    """
    
    @decorator
    def run_checkers(func, *args, **kwargs):
        ret = func(*args, **kwargs)
        
        if type(ret) != tuple:
            ret = (ret, )
        assert len(ret) == len(checkers_args)
        
        if checkers_args:
            for idx, checker_function in enumerate(checkers_args):
                if callable(checker_function):
                    result = checker_function(ret[idx])
        return ret
    return run_checkers