"""General module for various bases."""

import logging
import os

from tagterm.exceptions import ProcessError


EOL = "\n"    # end of line default character(s)

PROJECT = os.path.normpath(
    os.path.join(
        __file__,
        os.path.pardir,
        os.path.pardir
    )
)


def get_logger(name, debug=False):
    logging.basicConfig(
        filename="tagterm.log",
        format="%(levelname)s - %(asctime)s - %(message)s"
    )
    log = logging.getLogger(name)
    level = logging.DEBUG if debug else logging.INFO
    log.setLevel(level)
    return log


class BaseReadProcess(object):
    """Simple base for every process that needs to make read-only actions."""

    def __init__(self, path_in, debug=False):
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
        self._log = None
        self.debug = debug

    def load(self):
        self.log.info("Reading content of %s", self.path_in)
        with open(self.path_in) as stream:
            self.content = stream.read()

    @property
    def log(self):
        if not self._log:
            self._log = get_logger(__name__, debug=self.debug)
        return self._log


class BaseWriteProcess(BaseReadProcess):
    """Simple base for every process that needs to make writeable actions."""

    def __init__(self, path_in, path_out=None, **kwargs):
        super(BaseWriteProcess, self).__init__(path_in, **kwargs)

        path_out = path_out or os.path.dirname(os.path.normpath(self.path_in))
        path_out = os.path.abspath(path_out)
        if not os.path.isdir(path_out):
            self.log.warning("Creating output path %s", path_out)
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
        self.log.info("Saving content for %s", self.path_out)
        with open(self.path_out, "w") as stream:
            stream.write(self.content)
