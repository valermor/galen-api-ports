
class IllegalMethodCallException(Exception):
    """
    Thrown when a method is called on an object which is not in a right state.
    """
    def __init__(self, *args, **kwargs):
        super(IllegalMethodCallException, self).__init__(*args, **kwargs)


class FileNotFoundError(Exception):
    """
    A file was not found.
    """
    def __init__(self, *args, **kwargs):
        super(FileNotFoundError, self).__init__(*args, **kwargs)
