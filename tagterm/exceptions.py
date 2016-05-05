"""Custom exceptions module for error code return ability."""


def get_return_code(exc):
    if not exc:
        return 0    # all good
    if isinstance(exc, BaseError):
        return exc.CODE    # known error
    return BaseError.CODE    # internal error code


class BaseError(Exception):
    """Base exception class for all particular and derived errors."""

    CODE = 1    # generic code used for unhandled thrown exceptions


class ProcessError(BaseError):
    """Generic exception for any aspect of a processing class."""

    CODE = 2


class ConvertError(ProcessError):
    """Conversion related errors."""

    CODE = 10


class RemoveError(ProcessError):
    """Tags removal related errors."""

    CODE = 20


class ValidateError(ProcessError):
    """Markup validation related errors."""

    CODE = 30
