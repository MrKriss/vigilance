

class SchemaConditionError(Exception):
    """ A target conditon was found unacceptable for a field """


class RangeInvalid(Exception):
    """ The value is not in the given range """    


class MinInvalid(Exception):
    """ The value is below the specified minimum """    


class MaxInvalid(Exception):
    """ The value is above the specifeid maximum """    




# class Invalid(Exception):
#     """ Base Exception to capture invalid conditions.

#     :attr msg: The error message from the codition tested.
#     :attr error_message: The actual error message that was raised, as a
#         string.

#     Example called with: 
#         raise RangeInvalid(msg or 'value must be higher than %s' % min)

#     """

#     def __init__(self, message, path=None, error_message=None, error_type=None):
#         super().__init__(self, message)
#         self.error_message = error_message or message

#     # @property
#     # def msg(self):
#     #     # Simply return the msg passed to the exception 
#     #     return self.args[0]

#     # def __str__(self):
#     #     path = ' @ data[%s]' % ']['.join(map(repr, self.path)) \
#     #         if self.path else ''
#     #     output = Exception.__str__(self)
#     #     if self.error_type:
#     #         output += ' for ' + self.error_type
#     #     return output + path




# class RequiredFieldInvalid(Invalid):
#     """Required field was missing."""


# class ObjectInvalid(Invalid):
#     """The value we found was not an object."""


# class DictInvalid(Invalid):
#     """The value found was not a dict."""


# class ExclusiveInvalid(Invalid):
#     """More than one value found in exclusion group."""


# class InclusiveInvalid(Invalid):
#     """Not all values found in inclusion group."""


# class SequenceItemInvalid(Invalid):
#     """One of the values found in a sequence was invalid."""


# class SequenceTypeInvalid(Invalid):
#     """The type found is not a sequence type."""


# class TypeInvalid(Invalid):
#     """The value was not of required type."""


# class ValueInvalid(Invalid):
#     """The value was found invalid by evaluation function."""


# class ScalarInvalid(Invalid):
#     """Scalars did not match."""


# class CoerceInvalid(Invalid):
#     """Impossible to coerce value to type."""


# class AnyInvalid(Invalid):
#     """The value did not pass any validator."""


# class AllInvalid(Invalid):
#     """The value did not pass all validators."""


# class MatchInvalid(Invalid):
#     """The value does not match the given regular expression."""


# class RangeInvalid(Invalid):
#     """The value is not in given range."""

# class TrueInvalid(Invalid):
#     """The value is not True."""


# class FalseInvalid(Invalid):
#     """The value is not False."""


# class BooleanInvalid(Invalid):
#     """The value is not a boolean."""


# class UrlInvalid(Invalid):
#     """The value is not a url."""


# class FileInvalid(Invalid):
#     """The value is not a file."""


# class DirInvalid(Invalid):
#     """The value is not a directory."""


# class PathInvalid(Invalid):
#     """The value is not a path."""


# class LiteralInvalid(Invalid):
#     """The literal values do not match."""



