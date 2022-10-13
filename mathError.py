from typing import Tuple


class MathError(Exception):
    def __init__(self, inputString: str, span: Tuple[int, int], message: str):
        super().__init__(
            {"inputString": inputString, "span": span, "error": inputString[span[0]:span[1]], "message": message})

    def __str__(self) -> str:
        return super().__repr__()


class MathParserError(MathError):
    def __init__(self, inputString: str, span: Tuple[int, int], message: str):
        super().__init__(inputString, span, message)


class MathTokenizerError(MathError):
    def __init__(self, inputString: str, span: Tuple[int, int], message: str):
        super().__init__(inputString, span, message)


class MathComputeError(MathError):
    def __init__(self, inputString: str, span: Tuple[int, int], message: str):
        super().__init__(inputString, span, message)
