#!/usr/bin/env python3
"""Provide a simple lexer based on regular expressions."""
import re
from typing import List, Pattern


class Token:
    """Represent a token of a text."""

    def __init__(self, identifier: str = '', content: str = '', position: int = -1, lineno: int = -1) -> None:
        """
        Initialize.

        :param identifier: of the token
        :param content: text content of the token
        :param position: column in line (starting from zero)
        :param lineno: line in text (starting from zero)
        """
        self.identifier = identifier
        self.content = content
        self.position = position
        self.lineno = lineno

    def __repr__(self) -> str:
        """Represent token as a constructor."""
        return 'Token({!r}, {!r}, {}, {})'.format(self.identifier, self.content, self.position, self.lineno)

    def __eq__(self, other: object) -> bool:
        """Check that tokens are equal by comparing their fields."""
        if not isinstance(other, Token):
            return False

        return self.identifier == other.identifier and self.lineno == other.lineno and \
               self.position == other.position and self.content == other.content


class Rule:
    """Define a lexing rule."""

    def __init__(self, identifier: str, pattern: Pattern) -> None:
        """
        Initialize.

        :param identifier: of the rule
        :param pattern: regular expression defining the rule
        """
        self.identifier = identifier
        self.pattern = pattern


NONTAB_RE = re.compile(r'[^\t]')


class Error(Exception):
    """Is raised when no token rule applies."""

    def __init__(self, line: str, position: int, lineno: int) -> None:
        """
        Initialize.

        :param line: line that caused the error
        :param position: problematic position in the line (i.e. column), starting from zero
        :param lineno: line number in the text (starting from zero)
        """
        self.line = line
        self.position = position
        self.lineno = lineno

        super().__init__()

    def __str__(self) -> str:
        """Represent the error with a nice pointer as a multi-line message."""
        pointer = re.sub(NONTAB_RE, ' ', self.line[:self.position]) + '^'
        txt = 'Unmatched text at line {} and position {}:\n{}\n{}'.format(self.lineno, self.position, self.line,
                                                                          pointer)
        return txt


WHITESPACE_RE = re.compile(r'\s')


class Lexer:
    """Lex the text given the rules table."""

    def __init__(self, rules: List[Rule], skip_whitespace: bool = False) -> None:
        """
        Initialize.

        :param rules: to match the tokens
        """
        self.rules = rules
        self.skip_whitespace = skip_whitespace

    def lex(self, text: str) -> List[List[Token]]:
        """
        Lex the given text.

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
                        break

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
