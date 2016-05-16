.. _usage:

Usage
=====

After completing the :ref:`installation <installation>` procedures,
you can use the available or prebuilt **tagterm** executable alone or
under the Java wrapper found under the *src* directory. Check *src/Main.java*
as an example of handling the *src/tagterm* Java package.


Python
------

On Windows, make sure that you have added your paths of interest properly
under the `PATH` system environment variable or just use `python tagterm`
under *bin* instead of `tagterm` when executing it as Python code. It is
recommended to use the prebuilt executable called **tagterm.exe**.

.. code-block:: bash

    # List of available commands.
    tagterm --help

    # Validate and convert HTML file to XHTML with permissive level 1.
    tagterm -v validate -i res/error.html -p
    tagterm -v convert -i res/error.html -p
    # Check and watch out for nonzero exit codes.
    tail tagterm.log

    # Now remove tags from the XHTML file.
    tagterm -v remove -i res/error-convert.xhtml
    cat res/error-convert-remove.xml    # everything ok

.. note::
    The `-v` flag stands for *verbose* and you can also use `-o` option for
    putting the output in a separate path. Run with `-h` for more info, based
    on the chosen command.


Java
----

As you can see in *src/Main.java* example you can simple validate a HTML file
by running this (after importing the `tagterm` package):

.. code-block:: java

    Tagterm tagterm = new Tagterm("tagterm");
    tagterm.validate("res/error.html");

For conversion, removal and their [s]tring relatives, please consult the
:ref:`API <java_api>`.


Tags
----

For editing the tags configuration file, you have to edit the
*etc/tagterm/tags* file accordingly, then loading the new settings into your
previously setup installed package to make a new build based on new settings.

1. Edit **tags** file.
2. Run `./setup.sh` or `setup.bat` again.
3. :ref:`Build <build>` again.
4. Use the newly created *bin/dist/tagterm* executable.
