========================
pytest-find-dependencies
========================

.. image:: https://img.shields.io/pypi/v/pytest-find-dependencies.svg
    :target: https://pypi.org/project/pytest-find-dependencies
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-find-dependencies.svg
    :target: https://pypi.org/project/pytest-find-dependencies
    :alt: Python versions

.. image:: https://github.com/mrbean-bremen/pytest-find-dependencies/workflows/Testsuite/badge.svg
    :target: https://github.com/mrbean-bremen/pytest-find-dependencies/actions?query=workflow%3ATestsuite
    :alt: Test suite

.. image:: https://codecov.io/gh/mrbean-bremen/pytest-find-dependencies/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/mrbean-bremen/pytest-find-dependencies
    :alt: Code coverage

A pytest plugin to find dependencies between tests.

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with
`@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Summary
-------

Tests shall generally not depend on each other. To ensure this, plugins
like `pytest-randomly`_ or  `pytest-reverse`_ are commonly used. These
plugins find dependent tests, but it is up to you to find which test they
are depend upon.

The plugin aims to automate this task. Dependencies are found
in the first place by running all tests in forward and backwards direction
and checking if any tests fail if executed in one order but not in the other.
This will find most (but not all) test dependencies (the same way as
`pytest-reverse`_). If any dependent test is found, more test runs with
a subset of all tests are run using binary search, until a test is found
that causes the other test to fail.

Running tests this way may be time-consuming, especially with many tests, so it
is recommended to run this only once in a while.

Installation
------------

You can install "pytest-find-dependencies" via `pip`_ from `PyPI`_::

    $ pip install pytest-find-dependencies

Usage
-----

If the plugin is installed, it can be used by adding the pytest option
`--find-dependencies`. After running all needed tests, all found
dependencies are listed. Here is an example::

    =================================================
    Run dependency analysis for 7 tests.
    Executed 19 tests in 4 test runs.
    Dependent tests:
    test_one.py::test_b depends on test_one.py::test_e
    =================================================

In this case 7 tests have been analyzed, one dependent test has been found
after running the tests forwards and backwards, and after 2 additional test
runs with an overall of 5 tests, the test it depended on was found.

Limitations
-----------
Only dependencies are found that are reset with a new test run. If a test
changes the environment permanently (for example by setting environment
variables that are never reset), the dependency will not be found by this
plugin.

If you have installed `pytest-randomly`_, it will normally randomly reorder
all tests. The plugin is disabled while running with `--find-dependencies`,
and it is currently not possible to use fixed seed to start with a certain
test order (may be added later).

Other re-ordering plugins are currently not taken into account, so ordering
tests manually will not change the outcome.

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license,
"pytest-find-dependencies" is free and open source software.


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/mrbean-bremen/pytest-find-dependencies/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`pytest-randomly`: https://github.com/pytest-dev/pytest-randomly
.. _`pytest-reverse`: https://github.com/adamchainz/pytest-reverse
