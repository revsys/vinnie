import warnings

from pathlib import Path
from urllib.parse import urlparse

from .exceptions import VinnieConfigError

ALLOWED_OPTIONS = [
    "push",
    "repo",
    "repo_url",
    "ssh_key",
    "github_token",
    "gitlab_token",
    "prefix",
    "omit_prefix",
    "semver",
    "s3_access_key",
    "s3_secret_key",
    "s3_url",
    "current_version",
    "remote",
    "marker",
]


class VinnieConfig:
    """
    Configuration validation
    """

    def __init__(self, **kwargs):
        # Set object properties from all kwargs
        for key in ALLOWED_OPTIONS:
            setattr(self, key, kwargs.get(key, None))

        # Ensure we don't have any invalid items
        for key in kwargs:
            if key not in ALLOWED_OPTIONS:
                raise VinnieConfigError(f"Unknown option: {key}")

        # Default to using semver
        if self.semver is None:
            self.semver = True

        # Default to not using omit-prefix
        if self.omit_prefix is None:
            self.omit_prefix = False

        # Default to using 'origin' as the remote
        if self.remote is None:
            self.remote = "origin"

    def validate(self):
        """ Validate that the provided options make sense """

        # Validate our repo setup is correct
        self.validate_repo()

        # Validate keys and tokens
        self.validate_keys_and_tokens()

        # Validate s3 options
        self.validate_s3()

        return True

    def validate_repo(self):
        """ Ensure we given a repo path or URL """
        # We can only have a repo path or a repo URL, but not both
        if self.repo_url is not None and self.repo is not None:
            raise VinnieConfigError(
                "Cannot set repo url and repo path at the same time"
            )

        # Ensure if we have a path, that it exists
        if not self.repo_url:
            self.validate_repo_path()
        else:
            self.validate_repo_url()

    def validate_repo_path(self):
        """ Ensure our repo path exists, is readable, and looks to be a git repo """
        p = Path(self.repo)

        if not p.exists():
            raise VinnieConfigError(f"Repository Path '{self.repo}' does not exist.")

        if not p.is_dir():
            raise VinnieConfigError(
                f"Repository Path '{self.repo}' is not a directory."
            )

        # Ensure path has a `.git` directory in it:
        found_git_dir = False

        for child in p.iterdir():
            if child.name == ".git" and child.is_dir():
                found_git_dir = True
                break

        if not found_git_dir:
            raise VinnieConfigError(
                f"Repository Path '{self.repo}' does not appear to be a git repo'"
            )

    def validate_keys_and_tokens(self):
        """ Ensure we have an SSH key or a token, but not more than we need """
        if any((self.ssh_key, self.github_token, self.gitlab_token)):
            warnings.warn("SSH and API token features not yet implemented")

    def validate_repo_url(self):
        """ Ensure repo URL looks valid """
        try:
            parts = urlparse(self.repo_url)

            if not (parts.scheme == "http" or parts.scheme == "https"):
                raise ValueError

            if not parts.netloc:
                raise ValueError

        except ValueError:
            raise VinnieConfigError(f"'{self.repo_url}' is not a valid URL")

    def validate_s3(self):
        # We either need no s3 options or all of them
        s3_options = (self.s3_access_key, self.s3_secret_key, self.s3_url)
        if any(s3_options) and not all(s3_options):
            raise VinnieConfigError("Some, but not all S3 options set")

    def dump(self):
        for k, v in self.__dict__.items():
            print(f"{k}={v}")

