#!/usr/bin/env python3
"""
Provides a simple lexer based on regular expressions.
"""
import re
from typing import List, Pattern


class Token:
    """
    Represents a token of a text.
    """

    def __init__(self, identifier: str = '', content: str = '', position: int = -1, lineno: int = -1) -> None:
        self.identifier = identifier
        self.content = content
        self.position = position
        self.lineno = lineno

    def __repr__(self) -> str:
        return 'Token({!r}, {!r}, {}, {})'.format(self.identifier, self.content, self.position, self.lineno)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False

        return self.identifier == other.identifier and self.lineno == other.lineno and \
               self.position == other.position and self.content == other.content


class Rule:
    """
    Defines a lexing rule.
    """

    def __init__(self, identifier: str, pattern: Pattern) -> None:
        self.identifier = identifier
        self.pattern = pattern


NONTAB_RE = re.compile(r'[^\t]')


class Error(Exception):
    """
    Raised when no token rule applies.
    """

    def __init__(self, line: str, position: int, lineno: int) -> None:
        self.line = line
        self.position = position
        self.lineno = lineno

        super().__init__()

    def __str__(self) -> str:
        pointer = re.sub(NONTAB_RE, ' ', self.line[:self.position]) + '^'
        txt = 'Unmatched text at line {} and position {}:\n{}\n{}'.format(self.lineno, self.position, self.line,
                                                                          pointer)
        return txt


WHITESPACE_RE = re.compile(r'\s')


class Lexer:
    """
    Lexes the text given the rules table.
    """

    def __init__(self, rules: List[Rule], skip_whitespace: bool = False) -> None:
        """
        :param rules: to match the tokens
        """
        self.rules = rules
        self.skip_whitespace = skip_whitespace

    def lex(self, text: str) -> List[List[Token]]:
        """
        Lexes the text.

        :param text: to be lexed.
        :return: list of matched tokens
        """
        lines = text.splitlines()
        tokens = []  # type: List[List[Token]]

        for lineno, line in enumerate(lines):
            line_tokens = []

            position = 0
            while position < len(line):
                mtched = False
                for rule in self.rules:
                    mtch = rule.pattern.match(line, position)
                    if mtch:
                        token = Token(
                            identifier=rule.identifier, content=mtch.group(), position=position, lineno=lineno)
                        line_tokens.append(token)

                        position = mtch.end()
                        mtched = True

                if not mtched:
                    if self.skip_whitespace:
                        mtch = WHITESPACE_RE.match(line, position)
                        if mtch:
                            position = mtch.end()
                            mtched = True

                if not mtched:
                    raise Error(line=line, position=position, lineno=lineno)

            tokens.append(line_tokens)

        return tokens
