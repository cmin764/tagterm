"""Handles everything dealing with conversion operations."""

from tagterm.base import BaseWriteProcess
from tagterm.exceptions import ConvertError


class Converter(BaseWriteProcess):

    def convert(self):
        raise ConvertError("could not convert")
