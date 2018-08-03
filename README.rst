Lexery
======
A simple lexer based on regular expressions.

Inspired by https://eli.thegreenplace.net/2013/06/25/regex-based-lexical-analysis-in-python-and-javascript

Usage
=====
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
    >>>
    >>> tokens = lexer.lex(text=text)
    >>> tokens
    [[Token('identifier', 'crop', 0, 0), Token('lpar', '(', 9, 0), Token('number', '20', 11, 0),
    Token('comma', ',', 13, 0), Token('number', '30', 15, 0), Token('comma', ',', 17, 0),
    Token('number', '40', 19, 0), Token('comma', ',', 21, 0), Token('number', '10', 23, 0), Token('rpar', ')', 26, 0),
    Token('semi', ';', 28, 0)]]
