"""General module for various bases."""

import logging
import os

from tagterm.exceptions import ProcessError


class BaseReadProcess(object):
    """Simple base for every process that needs to make read-only actions."""

    def __init__(self, path_in):
        if not os.path.isfile(path_in):
            raise ProcessError("invalid file path")
        self.path_in = path_in
        bname = os.path.basename(path_in)
        chunks = bname.rsplit(".", 1)
        if len(chunks) == 1:
            chunks += [None]
        self.file_name = chunks[0]
        self.file_ext = chunks[1]

        self.content = None

    def load(self):
        logging.info("Reading content of %s", self.path_in)
        with open(self.path_in) as stream:
            self.content = stream.read()


class BaseWriteProcess(BaseReadProcess):
    """Simple base for every process that needs to make writeable actions."""

    def __init__(self, path_in, path_out=None):
        super(BaseWriteProcess, self).__init__(path_in)

        path_out = path_out or os.path.dirname(os.path.normpath(self.path_in))
        if not os.path.isdir(path_out):
            logging.warning("Creating output path %s", path_out)
            os.makedirs(path_out)
        fname = self.get_file_name()
        ext = self.get_file_ext()
        if ext:
            fname += "." + ext
        self.path_out = os.path.join(path_out, fname)

    def get_file_name(self):
        return self.file_name

    def get_file_ext(self):
        return self.file_ext

    def save(self):
        logging.info("Saving content for %s", self.path_out)
        with open(self.path_out, "w") as stream:
            stream.write(self.content)
