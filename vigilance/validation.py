''' Implements capturing expressions of failed assertions 

Functions like a delayed assert, but where any failed expressions are logged 
and then all can be recalled at a later time in a pretty printed report. 

Routines
--------
expect(*exprs)
report_failures(print=True, clear=False)

Example
-------
Api is though using expect to test assertions in a dedicated custom checking function,
and then using report_failures to trigger the reporting at a later date.::

    def check_df(df):

        expect(
            (len(df) > 10, 'Number of rows is less than or equal to 10'),
            (df['A'].all(), 'All elements of column A are not True')
        ) 

        report_failures()


    check_df(df)

Example of generated output:: 

    Failed Expectations: 2

    1: File foo.py, line 3 in check_df()
        "len(df) > 10" is not True 
            -- Number of rows is less than or equal to 10  

    2: File foo.py, line 4 in check_df()
        "df['A'].all()" is not True 
            -- All elements of column A are not True  

See Also
--------
accepts: Decorator for associating custom checking functions with other function inputs. 
returns: Decorator for associating custom checking functions with other function outputs. 
'''

import inspect
import os.path
import ast
import astor

import numpy as np 


_failed_expectations = []


def expect(*exprs):
    """Tests given sequence of conditions and stores results.
    
    Parameters
    ----------
    exprs: bool or tuple of (bool, str)
        Variable number of expressions evaluated. If a tuple first element is 
        expression evaluated, second is the message displayed on failure in the report.   
    """

    # Catch case of only two arguments where one is expr and other is msg
    if len(exprs) == 2:
        if isinstance(exprs[0], (bool, np.bool_)) and isinstance(exprs[1], str):
            if not exprs[0]:
                _log_failure(arg_num=0, msg=exprs[1])
    else:
        for i, arg in enumerate(exprs):
            if isinstance(arg, (bool, np.bool_)):
                # Just an epression on its own 
                if not arg:
                    _log_failure(arg_num=i)
            elif isinstance(arg, (list, tuple)):
                if len(arg) != 2:
                    raise ValueError('Arguments must be either an expression,'
                                     ' or a tuple of length two as (expression, error_message)')
                expr, msg = arg
                if not expr:
                    _log_failure(arg_num=i, msg=msg)

def report_failures(print=True, clear=False):
    """ Print details of logged failures in expect function

    Parameters
    ----------
    print: bool
        If True, will print the failure report as well as returning it as a string.
    clear: bool
        If True, all logged failured will be cleared after being reported. 

    Returns
    -------
    string 
        The string formated failure report.
     """
        
    global _failed_expectations

    output = []

    if _failed_expectations:
        output.append('\nFailed Expectations: %s\n\n' % len(_failed_expectations))

        for i, failure in enumerate(_failed_expectations, start=1):

            report_line = '{idx}: File {file}, line {line}, in {funcname}()\n    "{expression}" is not True\n'

            if failure['msg']:
                report_line += '        -- {msg}\n'

            report_line += '\n'

            failure['idx'] = i
            output.append(report_line.format(**failure))

        if clear:
            _failed_expectations = []
    else:
        print("All Expectations Met.")

    print(''.join(output))

    return ''.join(output)


def _log_failure(arg_num, msg=None):
    """ Retrace stack and log the failed expresion information """

    # stack() returns a list of frame records
    #   0 is the _log_failure() function
    #   1 is the expect() function 
    #   2 is the function that called expect(), that's what we want
    #
    # a frame record is a tuple like this:
    #   (frame, filename, line, funcname, contextlist, index)
    # we're only interested in the first 4. 
    frame,  filename, file_lineno, funcname = inspect.stack()[2][:4]
    # Note that a frame object should be deleted once used to be safe and stop possible 
    # memory leak due to circular referencing 
    try:
        frame_source_lines, frame_start_lineno = (inspect.getsourcelines(frame))  # do something with the frame
    finally:
        del frame

    filename = os.path.basename(filename)

    # Build abstract syntax tree from source of frame
    source_ast = ast.parse(''.join(frame_source_lines))

    # Locate the executed expect function 
    func_body = source_ast.body[0].body

    map_lineno_to_node = {}
    for idx, node in enumerate(func_body):
        map_lineno_to_node[node.lineno] = node
    
    last_lineno = file_lineno - frame_start_lineno + 1

    element_idx = [x for x in map_lineno_to_node.keys() if x <= last_lineno]
    element_idx = max(element_idx)

    expect_function_ast = map_lineno_to_node[element_idx]

    # Return the source code of the numbered argument
    arg = expect_function_ast.value.args[arg_num]
    line = arg.lineno
    if isinstance(arg, (ast.Tuple, ast.List)):
        expr = astor.to_source(arg.elts[0])
    else:
        expr = astor.to_source(arg)

    filename = os.path.basename(filename)

    failure_info = {'file': filename, 'line': line, 'funcname': funcname, 'msg': msg, 'expression': expr}

    _failed_expectations.append(failure_info)


