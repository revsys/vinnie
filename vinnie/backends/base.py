class BaseBackend:
    """
    Vinnie Backend
    """

    def __init__(self, *args, **kwargs):
        self.config = kwargs["config"]

    def get_current_version(self):
        raise NotImplementedError

    def tag_version(self, value, remote="origin"):
        raise NotImplementedError
