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

        iflag, oflag, cflag, lflag, cc = 0, 1, 2, 3, 6
        self.orig_attr = raw_mode[:]
        self.orig_attr[cc] = raw_mode[cc][:]

        raw_mode[iflag] &= ~(
            termios.IXON | termios.ICRNL | termios.BRKINT | termios.INPCK | termios.ISTRIP
        )
        raw_mode[oflag] &= ~(termios.OPOST)
        raw_mode[cflag] |= termios.CS8
        raw_mode[lflag] &= ~(termios.ECHO | termios.ICANON | termios.ISIG | termios.IEXTEN)
        raw_mode[cc][termios.VMIN] = 0
        raw_mode[cc][termios.VTIME] = 1

        termios.tcsetattr(stdin_fileno, termios.TCSAFLUSH, raw_mode)

    def disable(self) -> None:
        if self.orig_attr:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, self.orig_attr)


def run() -> int:
    raw_mode = RawMode()
    try:
        raw_mode.enable()
        while True:
            b = sys.stdin.buffer.read(1)
            rune = b[0] if b else 0
            if chr(rune) in STRING_PRINTABLE:
                print(f"{rune} ('{chr(rune)}')", end="\r\n")
            else:
                print(f"{rune}", end="\r\n")

            if b == b"q":
                break
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    finally:
        raw_mode.disable()

    return 0


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
