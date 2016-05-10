.. _installation:

Installation
============

The whole component is written in Python and needs this interpreter and some
external libraries and packages to run and build properly. On top of a final
Linux/Windows executable built upon this package, there's a Java source
under the `src` directory which acts as a wrapper over the Python
code/executable for doing some basic processes over (X)HTML files.
More details about the API :ref:`here <api>`.


Preparing the system
--------------------

*Linux*

.. code-block:: bash

    sudo apt update
    sudo apt install --upgrade python python-dev python-setuptools libtidy-dev
    sudo -H easy_install -U pip

*Windows*

1. Download and install Python interpreter: https://www.python.org/downloads/release/python-2711/
2. Install PIP: https://pip.pypa.io/en/stable/installing/

.. note::
    Tidy library dependency will be copied and registered by installing
    the package.


Clone & install
---------------

*Linux*

.. code-block:: bash

    git clone https://github.com/cmin764/tagterm.git
    cd tagterm

    sudo -H pip install -Ur requirements.txt
    sudo ./setup.sh

*Windows*

.. code-block:: batch

    git clone https://github.com/cmin764/tagterm.git
    cd tagterm

    pip install -Ur requirements.txt
    rem Run this as Administrator:
    setup.bat

.. note::
    You can also use *virtualenv(wrapper)* to install the package and
    related libraries.

In order to make sure that everything works as expected, refer to the
:ref:`usage <usage>` examples.


.. _build:

Build *tagterm* executable
--------------------------

For this to work properly, you have to really install the package (no develop)
and have the appropriate version of PyInstaller (see *requirements.txt*).

*Linux*/*Windows*

.. code-block:: bash

    cd bin
    pyinstaller -F tagterm
    stat dist/tagterm    # details about the built executable

And you'll find the built executable under this path: *dist/tagterm*.
You can copy it anywhere and use it as a standalone ELF/MZPE executable.
Also, you can use the prebuilt ones, available under *bin* directory:

    * tagterm (pure Python script)
    * tagterm.elf (Linux)
    * tagterm.exe (Windows)


Build Java wrapper
------------------

*Linux*

.. code-block:: bash

    cd src
    javac Main.java    # compile
    java Main tagterm ../res/error.html    # run a set of examples

    # Or just simple:
    ./main.sh tagterm ../res/error.html

*Windows*

.. code-block:: batch

    cd src
    javac Main.java
    java Main ..\bin\tagterm.exe ..\res\error.html

    # rem Run with Windows executable:
    main.bat ..\bin\tagterm.exe ..\res\error.html


And you should see no exception trace in case everything is fine.
Instead of `tagterm` you may use any of the `../bin/dist/tagterm*` built
executables (or prebuilt ones) suitable for your platform.
