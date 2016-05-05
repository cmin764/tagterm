"""Handles everything dealing with validating operations."""

import re

import tidylib

from tagterm.base import BaseReadProcess
from tagterm.exceptions import ValidateError


class Validator(BaseReadProcess):

    FAIL_MARKERS = [
        "Error",
    ]
    _NOT_PERMISSIVE = [
        "Warning",
    ]

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
    }

    def __init__(self, *args, **kwargs):
        self.permissive = kwargs.pop("permissive", None)
        super(Validator, self).__init__(*args, **kwargs)

        self.markers = self.FAIL_MARKERS[:]
        if not self.permissive:
            self.markers.extend(self._NOT_PERMISSIVE)

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
