.. _api:

API
===


Python
++++++

.. automodule:: tagterm
    :members:

    Common functions
    ----------------

    .. autofunction:: tagterm.get_logger
    .. autofunction:: tagterm.get_return_code

    Base classes
    ------------

    .. automodule:: tagterm.base
        :members:

    Process classes
    ---------------

    .. automodule:: tagterm.converter
        :members:
    .. autoclass:: tagterm.Converter
        :members:

    .. automodule:: tagterm.remover
        :members:
    .. autoclass:: tagterm.Remover
        :members:

    .. automodule:: tagterm.validator
        :members:
    .. autoclass:: tagterm.Validator
        :members:

    Exceptions
    ----------

    .. automodule:: tagterm.exceptions
        :members:


.. _java_api:

Java
++++

.. class:: tagterm.Tagterm(String path)

    `path` - Path to the main Python *tagterm* executable used for all the
    processes.

    .. method:: tagterm.Tagterm.convert(String file)

        Converts a validated HTML file into XHTML.
        Returns `String` meaning the converted file path.

    .. method:: tagterm.Tagterm.converts(String html)

        Same as `convert`, but accepts HTML and returns XHTML content.

    .. method:: tagterm.Tagterm.remove(String file)

        Removes all the tags under a XHTML file.
        Returns `String` meaning the removed-tags file path.

    .. method:: tagterm.Tagterm.removes(String html)

        Same as `remove`, but accepts XHTML and returns XML content.

    .. method:: tagterm.Tagterm.validate(String file)

        Validates a HTML file.
        Returns `boolean` as a status of the operation.

    .. method:: tagterm.Tagterm.validates(String html)

        Same as `validate`, but accepts HTML content.
