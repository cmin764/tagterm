"""Handles everything dealing with validating operations."""

import re

import tidylib

from tagterm.base import BaseReadProcess
from tagterm.exceptions import ValidateError


class Validator(BaseReadProcess):

    FAIL_MARKERS = [
        "Warning",
    ]

    def validate(self):
        document, errors = tidylib.tidy_document(
            self.content, options={"numeric-entities": 1}
        )

        for line in errors.splitlines():
            for marker in self.FAIL_MARKERS:
                pattern = r"line \d+ column \d+ - {}:".format(marker)
                if re.match(pattern, line, flags=re.IGNORECASE):
                    self.log.warning("Tidy errors:\n%s", errors)
                    raise ValidateError("invalid HTML content")
        self.log.info("Clean HTML document")

        return document
