Lexery
======
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
    ...         lexery.Rule(identifier='identifier', pattern=re.compile(r'[a-zA-Z_][a-zA-Z_]*')),
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
