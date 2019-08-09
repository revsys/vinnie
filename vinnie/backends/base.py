import re
import semver


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

    def strip_prefix(self, value):
        if self.config.prefix:
            value = re.sub(f"^{self.config.prefix}", "", value)
        return value

    def add_prefix(self, value):
        if self.config.prefix:
            value = f"{self.config.prefix}{value}"
        return value

    def validate_version(self, value):
        if value is None:
            return False

        # If we have a prefix and don't start with it, not a version
        if self.config.prefix and not value.startswith(self.config.prefix):
            return False

        # Strip off the prefix to apply regex
        value = re.sub(f"^{self.config.prefix}", "", value)

        m = re.fullmatch(
            r"""^
            \d+ |                    # For non-semver incrementing integers
            \d+\-\d+\-.{8} |         # non-semver describe tags
            \d+\.\d+\.\d+   |        # Normal semver
            \d+\.\d+\.\d+\-\d+\-.{8} # Normal semver describe tags
        $
        """,
            value,
            re.X,
        )

        if m is not None:
            return True
        else:
            return False

    def get_latest_tag(self):
        """ Return the latest version looking tag """
        # Grab ALL of the tags first
        tags = self.get_all_tags()

        # We need to find the first tag that looks like a version tag to
        # start comparing order with semver
        newest_version = None

        for t in tags:
            candidate = str(t)

            if self.validate_version(candidate):
                newest_version = candidate
                break

        # Now we can start sorting
        for t in tags:
            this_tag = str(t)

            if self.validate_version(this_tag):
                if (
                    semver.compare(
                        self.strip_prefix(this_tag), self.strip_prefix(newest_version)
                    )
                    == 1
                ):
                    newest_version = this_tag

        return newest_version

    def get_current_version(self):
        raise NotImplementedError

    def tag_version(self, value):
        raise NotImplementedError

    def get_all_tags(self):
        raise NotImplementedError

    def push(self, remote="origin"):
        raise NotImplementedError
