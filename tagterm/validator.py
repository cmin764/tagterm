"""Handles everything dealing with validating operations."""

import re

import tidylib

from tagterm.base import BaseReadProcess
from tagterm.exceptions import ValidateError


class Validator(BaseReadProcess):

    E_MARKER = "Error"
    W_MARKER = "Warning"

    TIDY_OPTIONS = {
        # XHTML instead of HTML4.
        "output-xhtml": 1,
        # Pretty; not too much of a performance hit.
        "indent": 1,
        # No tidy meta tag in output.
        "tidy-mark": 0,
        # No wrapping.
        "wrap": 0,
        # Help ensure validation.
        "alt-text": "",
        # Little sense in transitional for tool-generated markup.
        "doctype": 'strict',
        # May not get what you expect but you will get something.
        "force-output": 1,
        "numeric-entities": 1,
        # Support unicode.
        "char-encoding": "utf8",
        "input-encoding": "utf8",
        "output-encoding": "utf8",
    }

    def __init__(self, *args, **kwargs):
        self.permissive = kwargs.pop("permissive", 0)
        super(Validator, self).__init__(*args, **kwargs)

        self.markers = [self.E_MARKER, self.W_MARKER]
        if self.permissive > 0:
            self.markers.remove(self.W_MARKER)
            if self.permissive > 1:
                self.markers.remove(self.E_MARKER)

    def validate(self):
        document, errors = tidylib.tidy_document(
            self.content,
            options=self.TIDY_OPTIONS
        )

        for line in errors.splitlines():
            for marker in self.markers:
                pattern = r"line \d+ column \d+ - {}:".format(marker)
                if re.match(pattern, line, flags=re.IGNORECASE):
                    self.log.warning("Tidy report:\n%s", errors)
                    raise ValidateError("invalid HTML content")

        if self.permissive and errors:
            self.log.debug("Tidy report:\n%s", errors)
        self.log.info("Clean HTML document")
        return document    # return its XHTML version
