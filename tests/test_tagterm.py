import os
import unittest

import tagterm


DEBUG = True
FNAME = "error"


def get_res(name):
    return os.path.join(tagterm.PROJECT, "res", name)


def convert(name):
    converter = tagterm.Converter(
        get_res(name + ".html"),
        debug=DEBUG,
        permissive=1
    )
    converter.load()
    converter.convert()
    converter.save()


def remove(name):
    convert(name)
    remover = tagterm.Remover(
        get_res("{}-convert.xhtml".format(name)),
        debug=DEBUG
    )
    remover.load()
    remover.remove()
    remover.save()


class TestTagterm(unittest.TestCase):

    def test_convert(self):
        convert(FNAME)

        self.assertTrue(
            os.path.exists(
                get_res(
                    "{}-convert.xhtml".format(FNAME)
                )
            )
        )

    def test_remove(self):
        convert(FNAME)
        remove(FNAME)

        self.assertTrue(
            os.path.exists(
                get_res(
                    "{}-convert-remove.xml".format(FNAME)
                )
            )
        )

    def test_validate(self):
        validator = tagterm.Validator(
            get_res(FNAME + ".html"),
            debug=DEBUG,
            permissive=1
        )
        validator.load()
        validator.validate()
