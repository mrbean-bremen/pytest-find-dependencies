======================================
Changelog for pytest-find-dependencies
======================================

Unreleased
----------

Changes
~~~~~~~
* added Python 3.13 and removed EOL Python 3.7 and 3.8 from CI tests
* dropped support for pytest versions < 6.2.4

Infrastructure
~~~~~~~~~~~~~~
* replaced ``setup.py``/``cfg`` by ``pyproject.toml``


`0.5.3`_ (2024-03-16)
---------------------
Adds compatibility to pytest 8.

Infrastructure
~~~~~~~~~~~~~~
* added Python 3.11 and 3.12 to and removed Python 3.6 from CI tests
* added pytest 7 and 8 to CI tests, adapted tests to work with pytest 8

`0.5.2`_ (2022-04-09)
---------------------
Bugfix release.

Fixes
-----
* fixed crash when multiple "always failing" tests are detected (see `#6`_)

Infrastructure
~~~~~~~~~~~~~~
* added pytest 7.0 to CI tests
* skip tests using ``pytest-xdist`` if it is not installed (see `#7`_)

`0.5.1`_ (2022-01-16)
---------------------
Slightly improves test output.

Changes
~~~~~~~
* run the outer test in quiet mode to avoid confusing messages; the
  given verbosity is still used for the internal test runs

Fixes
~~~~~
* do not try to find dependencies with ``setup-only`` and ``setup-plan``
  options

Infrastructure
~~~~~~~~~~~~~~
* added CI tests for different pytest versions

`0.5.0`_ (2022-01-15)
---------------------
Improves usability, fixes double test runs.

Changes
~~~~~~~
* dropped support for pytest versions < 4.3.0

New Features
~~~~~~~~~~~~
* exit status is set to failed if dependent tests are found (see `#3`_)
* command line parameters are now passed to the internal test runs

Fixes:
~~~~~~
* ignore warnings in tests where they may change the outcome (see `#2`_)
* tests have been running twice in each test run
* if `pytest-xdist` is installed, it is ensured that it is not used for the
  tests, as it would compromise the test result

`0.4.1`_ (2021-12-26)
---------------------

Fixes:
~~~~~~
* prevent a crash that happened in a specific setup (see `#1`_)

`0.4.0`_ (2021-04-21)
---------------------
Added ``--markers-to-ignore`` option.

New Features
~~~~~~~~~~~~
* added the option ``--markers-to-ignore`` to allow to ignore tests with
  ordering markers
  
Infrastructure
~~~~~~~~~~~~~~
* add tests for Python 3.10

`0.3.0`_ (2021-04-18)
---------------------
Adds more information to the result.

New Features
~~~~~~~~~~~~
* check if a dependency is due to a permanent change and list these tests
  separately without trying to find the dependency (instead of listing an
  incorrect dependency)
* added option ``reversed-first`` to first execute the tests in reversed
  direction.

Changes
~~~~~~~
* do not disable ``pytest-randomly`` (no more needed after the change to
  separate processes)

`0.2.0`_ (2021-04-07)
---------------------
Makes finding dependencies more reliable.

New Features
~~~~~~~~~~~~
* dependencies happening on first run (instead of the reverse run) are also
  considered
* each test run is now executed in a separate process to minimize dependencies
  between test runs (makes the process slower, however)

Fixes
~~~~~
* disable ``pytest-randomly`` ordering if installed

`0.1.0`_ (2021-04-04)
---------------------

First PyPI release.

New Features
~~~~~~~~~~~~
* find dependencies in tests as long as they are based on the test modules
  themselves


.. _`0.1.0`: https://pypi.org/project/pytest-find-dependencies/0.1.0/
.. _`0.2.0`: https://pypi.org/project/pytest-find-dependencies/0.2.0/
.. _`0.3.0`: https://pypi.org/project/pytest-find-dependencies/0.3.0/
.. _`0.4.0`: https://pypi.org/project/pytest-find-dependencies/0.4.0/
.. _`0.4.1`: https://pypi.org/project/pytest-find-dependencies/0.4.1/
.. _`0.5.0`: https://pypi.org/project/pytest-find-dependencies/0.5.0/
.. _`0.5.1`: https://pypi.org/project/pytest-find-dependencies/0.5.1/
.. _`0.5.2`: https://pypi.org/project/pytest-find-dependencies/0.5.2/
.. _`0.5.3`: https://pypi.org/project/pytest-find-dependencies/0.5.3/
.. _`#1`: https://github.com/mrbean-bremen/pytest-find-dependencies/issues/1
.. _`#2`: https://github.com/mrbean-bremen/pytest-find-dependencies/issues/2
.. _`#3`: https://github.com/mrbean-bremen/pytest-find-dependencies/issues/3
.. _`#6`: https://github.com/mrbean-bremen/pytest-find-dependencies/issues/6
.. _`#7`: https://github.com/mrbean-bremen/pytest-find-dependencies/issues/7
