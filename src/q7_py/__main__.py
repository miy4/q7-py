from __future__ import annotations

import string
import sys
import termios

STRING_PRINTABLE = string.ascii_letters + string.digits + string.punctuation


class RawMode:
    orig_attr: list[int | bytes]

    def __init__(self) -> None:
        self.orig_attr = []

    def enable(self) -> None:
        stdin_fileno = sys.stdin.fileno()
        raw_mode = termios.tcgetattr(stdin_fileno)
        self.orig_attr = raw_mode[:]

        iflag, lflag = 0, 3
        raw_mode[iflag] &= ~(termios.IXON)
        raw_mode[lflag] &= ~(termios.ECHO | termios.ICANON | termios.ISIG | termios.IEXTEN)

        termios.tcsetattr(stdin_fileno, termios.TCSAFLUSH, raw_mode)

    def disable(self) -> None:
        if self.orig_attr:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, self.orig_attr)


def main() -> None:
    raw_mode = RawMode()
    try:
        raw_mode.enable()
        while (b := sys.stdin.buffer.read(1)) != b"q":
            rune = b[0]
            if chr(rune) in STRING_PRINTABLE:
                print(f"{rune} ('{chr(rune)}')")
            else:
                print(f"{rune}")

    finally:
        raw_mode.disable()

    sys.exit(0)


if __name__ == "__main__":
    main()
