========================
pytest-find-dependencies
========================

.. image:: https://img.shields.io/pypi/v/pytest-find-dependencies.svg
    :target: https://pypi.org/project/pytest-find-dependencies
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-find-dependencies.svg
    :target: https://pypi.org/project/pytest-find-dependencies
    :alt: Python versions

A pytest plugin to find dependencies between tests.

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with
`@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

The plugin aims to find dependencies between tests by running the tests
both in forwards and  backwards direction, and trying to find any
dependencies using a binary search. Note that the plugin is still work
in progress.

Installation
------------

You can install "pytest-find-dependencies" via `pip`_ from `PyPI`_::

    $ pip install pytest-find-dependencies

Usage
-----

If the plugin is installed, it can be used by adding the pytest option
`--find-dependencies`.

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
