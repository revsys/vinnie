import warnings

from git import Repo
from git.exc import GitCommandError

from .base import BaseBackend


class VinnieGit(BaseBackend):
    """ Local git backend for Vinnie """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo = Repo(self.config.repo)

    def get_current_version(self):
        """ Get the current version """
        try:
            return self.repo.git.describe(tags=True)
        except GitCommandError:
            return self.get_initial_version()

    def tag_version(self, value, remote="origin"):
        self.repo.create_tag(value, message=f"Version '{value}' set by vinnie")

        # See if we have a remote by that name
        try:
            remote = self.repo.remote(remote)
            remote.push()
        except ValueError:
            warnings.warn(
                f"Could not find git remote '{remote}'. Tag created, but not pushed."
            )
