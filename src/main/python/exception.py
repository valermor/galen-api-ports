
class NotReadyException(Exception):
    """
    Thrown when a method is called on an object which is not in a right state.
    """
    def __init__(self, *args, **kwargs):
        super(NotReadyException, self).__init__(*args, **kwargs)