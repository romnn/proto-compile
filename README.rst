===============================
proto-compile
===============================

.. image:: https://github.com/romnn/proto_compile/workflows/test/badge.svg
        :target: https://github.com/romnn/proto_compile/actions
        :alt: Build Status

.. image:: https://img.shields.io/pypi/v/proto_compile.svg
        :target: https://pypi.python.org/pypi/proto_compile
        :alt: PyPI version

.. image:: https://img.shields.io/github/license/romnn/proto_compile
        :target: https://github.com/romnn/proto_compile
        :alt: License

.. image:: https://codecov.io/gh/romnn/proto_compile/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/romnn/proto_compile
        :alt: Test Coverage

""""""""

Your short description here. 

.. code-block:: console

    $ pip install proto_compile

.. code-block:: python

    import proto_compile

Usage
-----

Dart:
Make sure you have Dart installed
.. code-block:: bash
  pub global activate protoc_plugin 

Development
-----------

For detailed instructions see the `contribution guide <CONTRIBUTING.rst>`_.

Tests
~~~~~~~
You can run tests with

.. code-block:: console

    $ invoke test
    $ invoke test --min-coverage=90     # Fail when code coverage is below 90%
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
