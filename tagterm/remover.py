"""Handles everything dealing with removing operations."""

from tagterm.base import BaseWriteProcess
from tagterm.exceptions import RemoveError


class Remover(BaseWriteProcess):

    def remove(self):
        raise RemoveError("invalid DOM")
