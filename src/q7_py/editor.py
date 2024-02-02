import string

from . import key
from .input import RawMode

STRING_PRINTABLE = string.ascii_letters + string.digits + string.punctuation


class Editor:
    raw_mode: RawMode

    def __init__(self) -> None:
        self.raw_mode = RawMode()

    def enter_raw_mode(self) -> None:
        self.raw_mode.enable()

    def leave_raw_mode(self) -> None:
        self.raw_mode.disable()

    def process_key_press(self) -> None:
        for rune in self.raw_mode.input_sequence():
            if rune == key.CTRL_Q:
                break
