class ResticException(Exception):
    def __init__(self, message: str, inner_exception: Exception | None = None):
        super().__init__(message)
        self.inner_exception: Exception | None = inner_exception

    def __str__(self) -> str:
        if self.inner_exception:
            return f"{super().__str__()} (Caused by {repr(self.inner_exception)})"
        return super().__str__()
