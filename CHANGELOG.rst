======================================
Changelog for pytest-find-dependencies
======================================

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
.. _`#1`: https://github.com/mrbean-bremen/pytest-find-dependencies/issues/1
.. _`#2`: https://github.com/mrbean-bremen/pytest-find-dependencies/issues/2
.. _`#3`: https://github.com/mrbean-bremen/pytest-find-dependencies/issues/3
