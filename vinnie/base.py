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

    def strip_prefix(self, value):
        if self.config.prefix:
            value = re.sub(f"^{self.config.prefix}", "", value)
        return value

    def omit_prefix(self, value):
        if self.config.omit_prefix:
            value = self.strip_prefix(value)
        return value

    def add_prefix(self, value):
        if self.config.prefix:
            value = f"{self.config.prefix}{value}"
        return value

    def version(self):
        """ Return the current version """
        if self.config.current_version is not None:
            return self.config.current_version
        else:
            return self.backend.get_current_version()

    def get_next_bump(self):
        current = self.strip_prefix(self.version())
        next_integer = str(int(current) + 1)
        return self.add_prefix(next_integer)

    def get_next_patch(self):
        current = self.strip_prefix(self.version())
        return self.add_prefix(semver.bump_patch(current))

    def get_next_minor(self):
        current = self.strip_prefix(self.version())
        return self.add_prefix(semver.bump_minor(current))

    def get_next_major(self):
        current = self.strip_prefix(self.version())
        return self.add_prefix(semver.bump_major(current))

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
