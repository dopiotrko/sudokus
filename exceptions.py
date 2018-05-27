class FindFailed(BaseException):
    pass


class SolvingError(BaseException):
    pass


class Solved(BaseException):
    pass


class Return(BaseException):
    """Zdrfiniowany zamiast instukcji przerwania return"""
    pass
