==================================================
Pfff: PEP 517 build backend for Pipfile projects.
==================================================

Pfff is a PEP 517-compliant build backend for Pipfile projects. It is built
upon Thomas Kluyver's Flit_, but with the additional functionality to read
Pipfile for requirements, providing a one true dependency specification for
Python package projects that uses Pipfile to manage dependencies.

.. _Flit: https://flit.readthedocs.io/en/latest/


Usage
=====

Replace `setup.py` with a `pyproject.toml`, with the following build backend
specification::

    [build-system]
    requires = ['pfff']
    build-backend = 'pfff.build'

Structure your project, and add package metadata as specified in Flit_'s
documentation.


How
===

Pfff monkey-patches Flit's internals to append contents of your Pipfile's
`packages` and `dev-packages` sections into Flit's requirement specification,
and uses Flit to build the resulting packages.
