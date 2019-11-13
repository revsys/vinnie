import semver
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
            version = self.repo.git.describe(tags=True)
        except GitCommandError:
            version = self.get_initial_version()

        # If this looks to be a good version, use it otherwise
        # we need to dig back into older tags to find the most recent
        # version (semver or incrementing integer)
        if self.validate_version(version):
            return version
        else:
            version = self.get_latest_tag()
            if self.validate_version(version):
                return version
            else:
                return self.get_initial_version()

    def get_all_tags(self):
        """
        Get all of the tags from this git repository and find the largest
        version number
        """
        return self.repo.tags

    def tag_version(self, value):
        self.repo.create_tag(value, message=f"Version '{value}' set by vinnie")

    def push(self, remote):
        # See if we have a remote by that name
        try:
            remote = self.repo.remote(remote)
            remote.push()
        except ValueError:
            warnings.warn(
                f"Could not find git remote '{remote}'. Tag created, but not pushed."
            )
