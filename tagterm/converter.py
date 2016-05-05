"""Handles everything dealing with conversion operations."""

from tagterm.base import BaseWriteProcess
from tagterm.exceptions import ConvertError
from tagterm.validator import Validator


class Converter(BaseWriteProcess, Validator):

    def convert(self):
        """Validate and convert input file."""
        document = self.validate()
        self.content = document

    def get_file_name(self):
        return super(Converter, self).get_file_name() + "-convert"
