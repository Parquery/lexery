#!/usr/bin/env python3

# pylint: disable=missing-docstring
import re
import unittest

import lexery


class TestLexery(unittest.TestCase):
    def test_that_it_works(self):
        text = 'crop ( 20, 30, 40, 10 ) ;\n' \
               '\n' \
               'resize(40, 10);'

        lexer = lexery.Lexer(rules=[
            lexery.Rule(identifier='identifier', pattern=re.compile(r'[a-zA-Z_][a-zA-Z_]*')),
            lexery.Rule(identifier='lpar', pattern=re.compile(r'\(')),
            lexery.Rule(identifier='number', pattern=re.compile(r'[1-9][0-9]*')),
            lexery.Rule(identifier='rpar', pattern=re.compile(r'\)')),
            lexery.Rule(identifier='comma', pattern=re.compile(r',')),
            lexery.Rule(identifier='semi', pattern=re.compile(r';')),
            lexery.Rule(identifier='space', pattern=re.compile(r' '))
        ])

        tokens = lexer.lex(text=text)

        expected = [[
            lexery.Token('identifier', 'crop', 0, 0),
            lexery.Token('space', ' ', 4, 0),
            lexery.Token('lpar', '(', 5, 0),
            lexery.Token('space', ' ', 6, 0),
            lexery.Token('number', '20', 7, 0),
            lexery.Token('comma', ',', 9, 0),
            lexery.Token('space', ' ', 10, 0),
            lexery.Token('number', '30', 11, 0),
            lexery.Token('comma', ',', 13, 0),
            lexery.Token('space', ' ', 14, 0),
            lexery.Token('number', '40', 15, 0),
            lexery.Token('comma', ',', 17, 0),
            lexery.Token('space', ' ', 18, 0),
            lexery.Token('number', '10', 19, 0),
            lexery.Token('space', ' ', 21, 0),
            lexery.Token('rpar', ')', 22, 0),
            lexery.Token('space', ' ', 23, 0),
            lexery.Token('semi', ';', 24, 0)
        ], [], [
            lexery.Token('identifier', 'resize', 0, 2),
            lexery.Token('lpar', '(', 6, 2),
            lexery.Token('number', '40', 7, 2),
            lexery.Token('comma', ',', 9, 2),
            lexery.Token('space', ' ', 10, 2),
            lexery.Token('number', '10', 11, 2),
            lexery.Token('rpar', ')', 13, 2),
            lexery.Token('semi', ';', 14, 2)
        ]]

        self.assertEqual(expected, tokens)

    def test_skip_whitespace(self):
        text = 'crop \t   ( 20, 30, 40, 10 ) ;'

        lexer = lexery.Lexer(
            rules=[
                lexery.Rule(identifier='identifier', pattern=re.compile(r'[a-zA-Z_][a-zA-Z_]*')),
                lexery.Rule(identifier='lpar', pattern=re.compile(r'\(')),
                lexery.Rule(identifier='number', pattern=re.compile(r'[1-9][0-9]*')),
                lexery.Rule(identifier='rpar', pattern=re.compile(r'\)')),
                lexery.Rule(identifier='comma', pattern=re.compile(r',')),
                lexery.Rule(identifier='semi', pattern=re.compile(r';'))
            ],
            skip_whitespace=True)

        tokens = lexer.lex(text=text)

        expected = [[
            lexery.Token('identifier', 'crop', 0, 0),
            lexery.Token('lpar', '(', 9, 0),
            lexery.Token('number', '20', 11, 0),
            lexery.Token('comma', ',', 13, 0),
            lexery.Token('number', '30', 15, 0),
            lexery.Token('comma', ',', 17, 0),
            lexery.Token('number', '40', 19, 0),
            lexery.Token('comma', ',', 21, 0),
            lexery.Token('number', '10', 23, 0),
            lexery.Token('rpar', ')', 26, 0),
            lexery.Token('semi', ';', 28, 0)
        ]]

        self.assertEqual(expected, tokens)


if __name__ == '__main__':
    unittest.main()
