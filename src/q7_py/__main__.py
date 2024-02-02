import sys

from .editor import Editor


def run() -> int:
    editor = Editor()
    try:
        editor.enter_raw_mode()
        editor.process_key_press()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    finally:
        editor.leave_raw_mode()

    return 0


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
