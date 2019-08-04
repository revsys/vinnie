import pytest

from vinnie.backends.base import BaseBackend


def test_ensure_base_raises():
    b = BaseBackend(config={})

    with pytest.raises(NotImplementedError):
        b.get_current_version()

    with pytest.raises(NotImplementedError):
        b.tag_version(value="foo")
