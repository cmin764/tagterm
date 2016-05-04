"""Handles everything dealing with validating operations."""

from tagterm.base import BaseReadProcess
from tagterm.exceptions import ValidateError


class Validator(BaseReadProcess):

    def validate(self):
        raise ValidateError("invalid HTML content")
