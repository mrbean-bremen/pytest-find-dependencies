======================================
Changelog for pytest-find-dependencies
======================================

Unreleased
----------

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