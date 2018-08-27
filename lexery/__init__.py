#!/usr/bin/env python3
"""Provide a simple lexer based on regular expressions."""
import re
from typing import List, Pattern, Optional


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


class _Lexing:
    """Keep state of a single lexing."""

    def __init__(self, unmatched_identifier: Optional[str] = None) -> None:
        """
        Initialize.

        :param unmatched_identifier:
            if set, unmatched characters are accumulated and emitted in a token with this identifier.
        """
        self.unmatched_identifier = unmatched_identifier

        self.tokens = [[]]  # type: List[List[Token]]

        self._unmatched_accumulator = []  # type: List[str]
        self._unmatched_pos = -1
        self._unmatched_lineno = -1

    def emit_matched_token(self, token: Token) -> None:
        """Emit all accumulated unmatched characters as a unmatched token and emit this token."""
        if self._unmatched_accumulator:
            assert self.unmatched_identifier is not None

            self.tokens[-1].append(
                Token(
                    identifier=self.unmatched_identifier,
                    content=''.join(self._unmatched_accumulator),
                    position=self._unmatched_pos,
                    lineno=self._unmatched_lineno))

            self._unmatched_accumulator = []

        self.tokens[-1].append(token)

    def start_new_line(self) -> None:
        """Start a new token line."""
        if self._unmatched_accumulator:
            assert self.unmatched_identifier is not None

            self.tokens[-1].append(
                Token(
                    identifier=self.unmatched_identifier,
                    content=''.join(self._unmatched_accumulator),
                    position=self._unmatched_pos,
                    lineno=self._unmatched_lineno))

            self._unmatched_accumulator = []

        self.tokens.append([])

    def accumulate_unmatched(self, character: str, position: int, lineno: int) -> None:
        """Add the unmatched character to the unmatched accumulator."""
        if not self._unmatched_accumulator:
            self._unmatched_pos = position
            self._unmatched_lineno = lineno

        self._unmatched_accumulator.append(character)

    def finish(self) -> None:
        """Signal the end of the lexing."""
        if self._unmatched_accumulator:
            assert self.unmatched_identifier is not None

            self.tokens[-1].append(
                Token(
                    identifier=self.unmatched_identifier,
                    content=''.join(self._unmatched_accumulator),
                    position=self._unmatched_pos,
                    lineno=self._unmatched_lineno))

            self._unmatched_accumulator = []


class Lexer:
    """Lex the text given the rules table."""

    def __init__(self, rules: List[Rule], skip_whitespace: bool = False,
                 unmatched_identifier: Optional[str] = None) -> None:
        """
        Initialize.

        :param rules: to match the tokens
        :param skip_whitespace: if True, white-spaces are skipped
        :param unmatched_identifier:
            if set, unmatched characters are accumulated in a list and lexed as a token with the given identifier
        """
        self.rules = rules
        self.skip_whitespace = skip_whitespace
        self.unmatched_identifier = unmatched_identifier

    def lex(self, text: str) -> List[List[Token]]:
        """
        Lex the given text.

        :param text: to be lexed.
        :return: list of matched tokens
        """
        lines = text.splitlines()

        lexing = _Lexing(unmatched_identifier=self.unmatched_identifier)

        for lineno, line in enumerate(lines):
            position = 0
            while position < len(line):
                mtched = False
                for rule in self.rules:
                    mtch = rule.pattern.match(line, position)
                    if mtch:
                        token = Token(
                            identifier=rule.identifier, content=mtch.group(), position=position, lineno=lineno)

                        lexing.emit_matched_token(token=token)

                        position = mtch.end()
                        mtched = True
                        break

                if not mtched:
                    if self.skip_whitespace:
                        mtch = WHITESPACE_RE.match(line, position)
                        if mtch:
                            position = mtch.end()
                            mtched = True

                if not mtched and self.unmatched_identifier is not None:
                    lexing.accumulate_unmatched(character=line[position], position=position, lineno=lineno)
                    position += 1
                    mtched = True

                if not mtched:
                    raise Error(line=line, position=position, lineno=lineno)

            if lineno < len(lines) - 1:
                lexing.start_new_line()

        lexing.finish()

        return lexing.tokens
