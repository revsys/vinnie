import semver
import re
import click

from .backends import VinnieGit, VinnieGitHub, VinnieGitLab
from .config import VinnieConfig
from .exceptions import VinnieConfigError


class Vinnie:
    def __init__(self, **kwargs):
        # Set object properties from all kwargs
        self.config = VinnieConfig(**kwargs)
        self.validated = False
        self.backend = None
        self.validate()

    def validate(self):
        self.config.validate()
        self.validated = True
        self.setup_backend()

    def setup_backend(self):
        """ Based on our configuration, grab the appropriate backend """
        # We're already setup
        if self.backend is not None:
            return

        # If we aren't given a repo_url, we need the Git backend
        if not self.config.repo_url:
            self.backend = VinnieGit(config=self.config)

        # GitHub API backend
        if self.config.repo_url and self.config.github_token:
            self.backend = VinnieGitHub(config=self.config)

        # GitLab backend
        if self.config.repo_url and self.config.gitlab_token:
            self.backend = VinnieGitLab(config=self.config)

        # Whoops, couldn't find an appropriate backend
        if self.backend is None:
            raise VinnieConfigError("ERROR: Could not determine which backend to use")

    def dump(self):
        self.config.dump()


    def version_only(self, value):
        return self.strip_bread(value)

    def strip_prefix(self, value):
        if self.config.prefix:
            value = re.sub(f"^{self.config.prefix}", "", value)
        return value

    def strip_suffix(self, value):
        if self.config.suffix:
            value = re.sub(f"-{self.config.suffix}$", "", value)
        return value

    def omit_prefix(self, value):
        if self.config.omit_prefix:
            value = self.strip_prefix(value)
        return value

    def omit_bread(self, value):
        return self.omit_prefix(self.omit_suffix(value))

    def omit_suffix(self, value):
        if self.config.omit_suffix:
            value = self.strip_suffix(value)
        return value

    def add_prefix(self, value):
        if self.config.prefix:
            value = f"{self.config.prefix}{value}"
        return value

    def add_suffix(self, value):
        if self.config.suffix:
            value = f"{value}-{self.config.suffix}"
        return value

    def add_bread(self, value):
        return self.add_prefix(self.add_suffix(value))

    def strip_bread(self, value):
        return self.strip_prefix(self.strip_suffix(value))

    def version(self):
        """ Return the current version """
        if self.config.current_version is not None:
            return self.config.current_version
        else:
            return self.backend.get_current_version()

    def get_next_bump(self):
        current = self.strip_bread(self.version())
        next_integer = str(int(current) + 1)
        return self.add_bread(next_integer)

    def get_next_patch(self):
        current = self.version_only(self.version())
        new = semver.bump_patch(current)
        return self.add_bread(new)

    def get_next_minor(self):
        current = self.strip_bread(self.version())
        new = semver.bump_minor(current)
        return self.add_bread(new)

    def get_next_major(self):
        current = self.strip_bread(self.version())
        new = semver.bump_major(current)
        return self.add_bread(new)

    def push(self, remote):
        if self.config.push:
            self.backend.push(remote)
        else:
            click.echo("Skipping push.", err=True)

    def next_bump(self):
        next_value = self.get_next_bump()
        self.backend.tag_version(next_value)
        self.push(self.config.remote)
        return next_value

    def next_patch(self):
        next_value = self.get_next_patch()
        self.backend.tag_version(next_value)
        self.push(self.config.remote)
        return next_value

    def next_minor(self):
        next_value = self.get_next_minor()
        self.backend.tag_version(next_value)
        self.push(self.config.remote)
        return next_value

    def next_major(self):
        next_value = self.get_next_major()
        self.backend.tag_version(next_value)
        self.push(self.config.remote)
        return next_value
