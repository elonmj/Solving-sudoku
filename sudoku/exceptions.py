class InvalidDigitError(Exception):
    def __init__(self, digit: int) -> None:
        super().__init__(f"{digit} is not a valid digit. Enter a digit between 1 and 9.")
