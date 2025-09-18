class ValidationError(Exception):
    def __init__(self, message: str = None, attr: str = None, value: str = None):
        if message:
            super().__init__(message)
        elif attr and value:
            super().__init__(f"Invalid format for {attr}: {value}")
        else:
            super().__init__("Invalid")
