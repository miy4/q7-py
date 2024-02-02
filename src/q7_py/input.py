from __future__ import annotations

import sys
import termios
from typing import Iterator


class RawMode:
    orig_attr: list[int | list[bytes | int]]

    def __init__(self) -> None:
        self.orig_attr = []

    def enable(self) -> None:
        stdin_fileno = sys.stdin.fileno()
        raw_mode = termios.tcgetattr(stdin_fileno)
        self.orig_attr = termios.tcgetattr(stdin_fileno)

        iflag, oflag, cflag, lflag, cc = 0, 1, 2, 3, 6
        raw_mode[iflag] &= ~(
            termios.IXON | termios.ICRNL | termios.BRKINT | termios.INPCK | termios.ISTRIP
        )
        raw_mode[oflag] &= ~termios.OPOST
        raw_mode[cflag] |= termios.CS8
        raw_mode[lflag] &= ~(termios.ECHO | termios.ICANON | termios.ISIG | termios.IEXTEN)
        raw_mode[cc][termios.VMIN] = 0
        raw_mode[cc][termios.VTIME] = 1

        termios.tcsetattr(stdin_fileno, termios.TCSAFLUSH, raw_mode)

    def disable(self) -> None:
        if self.orig_attr:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, self.orig_attr)

    def input_sequence(self) -> Iterator[int]:
        while True:
            b = sys.stdin.buffer.read(1)
            yield b[0] if b else 0
