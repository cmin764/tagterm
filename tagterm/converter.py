"""Handles everything dealing with conversion operations."""

from xml.etree import ElementTree

from tagterm.base import BaseWriteProcess
from tagterm.exceptions import ConvertError
from tagterm.validator import Validator


class Converter(BaseWriteProcess, Validator):

    def convert(self):
        """Validate and convert input file."""
        document = self.validate()
        self.content = document

        try:
            self.log.info("Checking XHTML version")
            doc = ElementTree.fromstring(document)
            ElementTree.tostring(doc, method="html")
        except Exception as exc:
            raise ConvertError("invalid XHTML document ({})".format(exc))

    def get_file_name(self):
        return super(Converter, self).get_file_name() + "-convert"

    def get_file_ext(self):
        return "xhtml"
