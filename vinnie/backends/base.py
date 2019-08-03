class BaseBackend:
    """
    Vinnie Backend
    """

    def __init__(self, *args, **kwargs):
        self.config = kwargs["config"]

    def get_initial_version(self):
        """ Set our initial version number(s) """
        if self.config.semver:
            return "0.0.0"
        else:
            return "0"

    def get_current_version(self):
        raise NotImplementedError

    def tag_version(self, value, remote="origin"):
        raise NotImplementedError
