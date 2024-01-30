import sys
import termios


def enable_raw_mode() -> None:
    stdin_fileno = sys.stdin.fileno()
    raw_mode = termios.tcgetattr(stdin_fileno)
    lflag = 3
    raw_mode[lflag] &= ~termios.ECHO

    termios.tcsetattr(stdin_fileno, termios.TCSAFLUSH, raw_mode)


def main() -> None:
    enable_raw_mode()

    while sys.stdin.buffer.read(1) != b"q":
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
