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

You can install ``pytest-find-dependencies`` via `pip`_ from `PyPI`_::

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

Some dependencies can be due to a permanent change in the environment (for
example by adding a change to a database that is not reverted in subsequent
test runs). In this case, the dependency cannot be found reliably, and these
tests are listed separately::

    =================================================
    Run dependency analysis for 5 tests.
    Executed 11 tests in 3 test runs.
    Tests failing permanently after all tests have run:
    test_one.py::test_b
    =================================================

Dependencies due to a permanent change will only be found if the offending
test is run before the dependent test, otherwise the test will just fail both
times.

The option ``--reversed-first`` allows you to reverse the sequence of the
first two test runs.

The option ``--markers-to-ignore`` allows to define a comma-separated list
of marker names. Tests that have these markers will be ignored in the
analysis (e.g. not run at all). This can be used to exclude tests that have
markers that define the test order. Examples include ``dependency`` (from the
``pytest-dependency`` plugin), ``order`` (from ``pytest-order``) or
``depends`` (from ``pytest-depends``). To ignore all tests with a
``dependency`` marker, you can use::

  python -m pytest --find-dependencies --markers-to-ignore=dependency

Note that in this case you also won't find other tests depending on the
ordered markers.

Notes
-----
- command line options given in the test are passed to all test runs
  in dependency find mode
- if any dependent tests are found, the exit code of the pytest run will be
  set to 1
- if ``pytest-xdist`` is detected, it is ensured that the internal tests
  are not distributed, as this would break the dependency check
- after finishing all test runs and displaying the result, "no tests run"
  is currently displayed on the summary line - this can be safely ignored

Usage of ordering plugins
-------------------------
If you use plugins which change the test order using markers, theses will only
be applied in the first test run. The order of the following test runs is
solely defined by ``pytest-find-dependencies``. This means that if you use
ordering plugins like ``pytest-order``, the dependencies will still be
found, if you don't exclude these tests (which may or may not be wanted).
Using ``pytest-randomly`` will randomize the first test run and can be used
in combination with ``pytest-find-dependencies`` without problems.

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
If you encounter any problems or have a feature request, please
`file an issue`_ along with a detailed description.

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
