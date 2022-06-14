===============================
proto-compile
===============================

.. image:: https://github.com/romnn/proto-compile/workflows/test/badge.svg
        :target: https://github.com/romnn/proto-compile/actions
        :alt: Build Status

.. image:: https://img.shields.io/pypi/v/proto-compile.svg
        :target: https://pypi.python.org/pypi/proto-compile
        :alt: PyPI version

.. image:: https://img.shields.io/github/license/romnn/proto-compile
        :target: https://github.com/romnn/proto-compile
        :alt: License

.. image:: https://codecov.io/gh/romnn/proto-compile/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/romnn/proto-compile
        :alt: Test Coverage

""""""""

Your short description here. 

.. code-block:: console

    $ pip install proto-compile

Usage
-----

.. code-block:: python

    import proto_compile


Development
-----------

For detailed instructions see the `contribution guide <CONTRIBUTING.rst>`_.

Tests
~~~~~~~
You can run tests with

.. code-block:: console

    $ invoke test
    $ invoke type-check                 # Run mypy type checks

Linting and formatting
~~~~~~~~~~~~~~~~~~~~~~~~
Lint and format the code with

.. code-block:: console

    $ invoke format
    $ invoke lint

All of this happens when you run ``invoke pre-commit``.

Note
-----

This project is still in the alpha stage and should not be considered production ready.
