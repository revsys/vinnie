import os

from vinnie.base import Vinnie


def repo_path(relative):
    """ Build a relative path to our tests/ dir """
    current = os.path.dirname(__file__)
    return os.path.join(current, relative)


def test_version(repo):
    v = Vinnie(repo=repo)
    assert v.version() == "v0.0.2"


def test_add_prefix(repo):
    v = Vinnie(repo=repo, prefix="foo")
    assert v.add_prefix("3.0.0") == "foo3.0.0"

    v = Vinnie(repo=repo)
    assert v.add_prefix("3.0.0") == "3.0.0"


def test_strip_prefix(repo):
    v = Vinnie(repo=repo, prefix="v")
    assert v.strip_prefix("v1.0.0") == "1.0.0"


def test_current_version(repo):
    # When given a version, use that instead of whatever is found in the repo
    v = Vinnie(repo=repo, current_version="2.1.1")
    assert v.version() == "2.1.1"
    assert v.get_next_patch() == "2.1.2"


def test_repo_without_tags(empty_repo):
    """ This tests situations where there are no initial tags """
    v = Vinnie(repo=empty_repo)
    v.dump()
    assert v.version() == "0.0.0"
    assert v.get_next_patch() == "0.0.1"


def test_repo_without_tags_no_semver(empty_repo):
    """ This tests situations where there are no initial tags """
    v = Vinnie(repo=empty_repo, semver=False)
    v.dump()
    assert v.version() == "0"
    assert v.get_next_bump() == "1"
