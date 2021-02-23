import pytest

from vinnie.backends.base import BaseBackend
from vinnie.config import VinnieConfig


def test_ensure_base_raises():
    b = BaseBackend(config={})

    with pytest.raises(NotImplementedError):
        b.get_current_version()

    with pytest.raises(NotImplementedError):
        b.tag_version(value="foo")

    with pytest.raises(NotImplementedError):
        b.get_all_tags()


def test_validate_version():
    # Validate unprefixed versions
    b = BaseBackend(config=VinnieConfig())

    # Good values
    assert b.validate_version("1.2.3") is True
    assert b.validate_version("14") is True
    assert b.validate_version("0.0.0") is True
    assert b.validate_version("0.0.9-3-gf7a71f0") is True

    # Bad values
    assert b.validate_version("FeatureFreeze") is False
    assert b.validate_version("bug-147") is False
    assert b.validate_version("200-bugfix") is False

    # Validate prefixed versions
    b = BaseBackend(config=VinnieConfig(prefix="v"))

    # Good values
    assert b.validate_version("v1.2.3") is True
    assert b.validate_version("v14") is True
    assert b.validate_version("v0.0.0") is True
    assert b.validate_version("v0.0.9-3-gf7a71f0") is True

    # Bad values
    assert b.validate_version("FeatureFreeze") is False
    assert b.validate_version("bug-147") is False
    assert b.validate_version("200-bugfix") is False
    assert b.validate_version("vFeatureFreeze") is False
    assert b.validate_version("vbug-147") is False
    assert b.validate_version("v200-bugfix") is False


def test_add_prefix(repo):
    b = BaseBackend(config=VinnieConfig(prefix="foo"))
    assert b.add_prefix("3.0.0") == "foo3.0.0"

    b = BaseBackend(config=VinnieConfig())
    assert b.add_prefix("3.0.0") == "3.0.0"


def test_strip_prefix(repo):
    b = BaseBackend(config=VinnieConfig(prefix="v"))
    assert b.strip_prefix("v1.0.0") == "1.0.0"


def test_add_suffix(repo):
    b = BaseBackend(config=VinnieConfig(suffix="foo"))
    assert b.add_suffix("3.0.0") == "3.0.0foo"

    b = BaseBackend(config=VinnieConfig())
    assert b.add_suffix("3.0.0") == "3.0.0"


def test_strip_suffix(repo):
    b = BaseBackend(config=VinnieConfig(suffix="-beta"))
    assert b.strip_suffix("1.0.0-beta") == "1.0.0"

