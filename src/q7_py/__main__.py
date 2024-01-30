import sys


def main() -> None:
    while sys.stdin.buffer.read(1):
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
