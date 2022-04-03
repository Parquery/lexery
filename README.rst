Lexery
======

.. image:: https://github.com/Parquery/lexery/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/Parquery/lexery/actions/workflows/ci.yml
    :alt: Continuous integration

.. image:: https://coveralls.io/repos/github/Parquery/lexery/badge.svg?branch=master
    :target: https://coveralls.io/github/Parquery/lexery?branch=master
    :alt: Coverage

.. image:: https://badge.fury.io/py/lexery.svg
    :target: https://pypi.org/project/lexery/
    :alt: PyPI - version

.. image:: https://img.shields.io/pypi/pyversions/lexery.svg
    :target: https://pypi.org/project/lexery/
    :alt: PyPI - Python Version

A simple lexer based on regular expressions.

Inspired by https://eli.thegreenplace.net/2013/06/25/regex-based-lexical-analysis-in-python-and-javascript

Usage
=====
You define the lexing rules and lexery matches them iteratively as a look-up:

.. code-block:: python

    >>> import lexery
    >>> import re
    >>> text = 'crop \t   ( 20, 30, 40, 10 ) ;'
    >>>
    >>> lexer = lexery.Lexer(
    ...     rules=[
    ...         lexery.Rule(identifier='identifier',
    ...             pattern=re.compile(r'[a-zA-Z_][a-zA-Z_]*')),
    ...         lexery.Rule(identifier='lpar', pattern=re.compile(r'\(')),
    ...         lexery.Rule(identifier='number', pattern=re.compile(r'[1-9][0-9]*')),
    ...         lexery.Rule(identifier='rpar', pattern=re.compile(r'\)')),
    ...         lexery.Rule(identifier='comma', pattern=re.compile(r',')),
    ...         lexery.Rule(identifier='semi', pattern=re.compile(r';'))
    ...     ],
    ...     skip_whitespace=True)
    >>> tokens = lexer.lex(text=text)
    >>> assert tokens == [[
    ...     lexery.Token('identifier', 'crop', 0, 0), 
    ...     lexery.Token('lpar', '(', 9, 0),
    ...     lexery.Token('number', '20', 11, 0),
    ...     lexery.Token('comma', ',', 13, 0),
    ...     lexery.Token('number', '30', 15, 0),
    ...     lexery.Token('comma', ',', 17, 0),
    ...     lexery.Token('number', '40', 19, 0),
    ...     lexery.Token('comma', ',', 21, 0),
    ...     lexery.Token('number', '10', 23, 0),
    ...     lexery.Token('rpar', ')', 26, 0),
    ...     lexery.Token('semi', ';', 28, 0)]]

Mind that if a part of the text can not be matched, a ``lexery.Error`` is raised:

.. code-block:: python

    >>> import lexery
    >>> import re
    >>> text = 'some-identifier ( 23 )'
    >>>
    >>> lexer = lexery.Lexer(
    ...     rules=[
    ...         lexery.Rule(identifier='identifier', pattern=re.compile(r'[a-zA-Z_][a-zA-Z_]*')),
    ...         lexery.Rule(identifier='number', pattern=re.compile(r'[1-9][0-9]*')),
    ...     ],
    ...     skip_whitespace=True)
    >>> tokens = lexer.lex(text=text)
    Traceback (most recent call last):
    ...
    lexery.Error: Unmatched text at line 0 and position 4:
    some-identifier ( 23 )
        ^

If you specify an ``unmatched_identifier``, all the unmatched characters are accumulated in tokens with that identifier:

.. code-block:: python

    >>> import lexery
    >>> import re
    >>> text = 'some-identifier ( 23 )-'
    >>>
    >>> lexer = lexery.Lexer(
    ...     rules=[
    ...         lexery.Rule(identifier='identifier', pattern=re.compile(r'[a-zA-Z_][a-zA-Z_]*')),
    ...         lexery.Rule(identifier='number', pattern=re.compile(r'[1-9][0-9]*')),
    ...     ],
    ...     skip_whitespace=True,
    ...     unmatched_identifier='unmatched')
    >>> tokens = lexer.lex(text=text)
    >>> assert tokens == [[
    ...     lexery.Token('identifier', 'some', 0, 0),
    ...    lexery.Token('unmatched', '-', 4, 0),
    ...    lexery.Token('identifier', 'identifier', 5, 0),
    ...    lexery.Token('unmatched', '(', 16, 0),
    ...    lexery.Token('number', '23', 18, 0),
    ...    lexery.Token('unmatched', ')-', 21, 0)]]


Installation
============

* Install lexery with pip:

.. code-block:: bash

    pip3 install lexery

Development
===========

* Check out the repository.

* In the repository root, create the virtual environment:

.. code-block:: bash

    python3 -m venv venv3

* Activate the virtual environment:

.. code-block:: bash

    source venv3/bin/activate

* Install the development dependencies:

.. code-block:: bash

    pip3 install -e .[dev]

Pre-commit Checks
-----------------
We provide a set of pre-commit checks that run unit tests, lint and check code for formatting.

Namely, we use:

* `yapf <https://github.com/google/yapf>`_ to check the formatting.
* The style of the docstrings is checked with `pydocstyle <https://github.com/PyCQA/pydocstyle>`_.
* Static type analysis is performed with `mypy <http://mypy-lang.org/>`_.
* Various linter checks are done with `pylint <https://www.pylint.org/>`_.

Run the pre-commit checks locally from an activated virtual environment with development dependencies:

.. code-block:: bash

    ./precommit.py

* The pre-commit script can also automatically format the code:

.. code-block:: bash

    ./precommit.py  --overwrite


Versioning
==========
We follow `Semantic Versioning <http://semver.org/spec/v1.0.0.html>`_. The version X.Y.Z indicates:

* X is the major version (backward-incompatible),
* Y is the minor version (backward-compatible), and
* Z is the patch version (backward-compatible bug fix).
