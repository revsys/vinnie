import os
import shutil
import pytest

from git import Repo


@pytest.fixture
def repo():
    current_dir = os.path.dirname(__file__)
    repo_path = os.path.join(current_dir, "repo")
    file1_name = os.path.join(repo_path, "README.md")
    file2_name = os.path.join(repo_path, "another_file.txt")

    r = Repo.init(repo_path)

    open(file1_name, "wb").close()

    r.index.add(["README.md"])
    r.index.commit("First version")

    r.create_tag("v0.0.1")

    open(file2_name, "wb").close()

    r.index.add(["another_file.txt"])
    r.index.commit("Second version")
    r.create_tag("v0.0.2")
    yield repo_path

    # Clean up the repo
    shutil.rmtree(repo_path)


@pytest.fixture
def empty_repo():
    """ Create a repo without any tags """
    current_dir = os.path.dirname(__file__)
    repo_path = os.path.join(current_dir, "empty-repo")
    file1_name = os.path.join(repo_path, "README.md")

    r = Repo.init(repo_path)

    open(file1_name, "wb").close()

    r.index.add(["README.md"])
    r.index.commit("First version")

    yield repo_path

    # Clean up the repo
    shutil.rmtree(repo_path)


@pytest.fixture
def non_semver_repo():
    current_dir = os.path.dirname(__file__)
    repo_path = os.path.join(current_dir, "repo")
    file1_name = os.path.join(repo_path, "README.md")
    file2_name = os.path.join(repo_path, "another_file.txt")

    r = Repo.init(repo_path)

    open(file1_name, "wb").close()

    r.index.add(["README.md"])
    r.index.commit("First version")

    r.create_tag("v1")

    open(file2_name, "wb").close()

    r.index.add(["another_file.txt"])
    r.index.commit("Second version")
    r.create_tag("v2")
    yield repo_path

    # Clean up the repo
    shutil.rmtree(repo_path)


@pytest.fixture
def mixed_repo():
    """ Create a repo with version tags and other random tags """
    current_dir = os.path.dirname(__file__)
    repo_path = os.path.join(current_dir, "repo")
    file1_name = os.path.join(repo_path, "README.md")
    file2_name = os.path.join(repo_path, "another_file.txt")

    r = Repo.init(repo_path)

    open(file1_name, "wb").close()

    r.index.add(["README.md"])
    r.index.commit("First version")

    r.create_tag("v0.0.1")
    r.create_tag("some-other-tag")
    open(file2_name, "wb").close()

    r.index.add(["another_file.txt"])
    r.index.commit("Second version")
    r.create_tag("FeatureFreeze")
    r.create_tag("v0.0.2")

    yield repo_path

    # Clean up the repo
    shutil.rmtree(repo_path)


@pytest.fixture
def mixed_repo2():
    """
    Create a repo with version tags and other random tags, specifically having
    a non-version tag newer than the last version
    """
    current_dir = os.path.dirname(__file__)
    repo_path = os.path.join(current_dir, "repo")
    file1_name = os.path.join(repo_path, "README.md")
    file2_name = os.path.join(repo_path, "another_file.txt")

    r = Repo.init(repo_path)

    open(file1_name, "wb").close()

    r.index.add(["README.md"])
    r.index.commit("First version")

    r.create_tag("v0.0.1")
    r.create_tag("some-other-tag")
    open(file2_name, "wb").close()

    r.index.add(["another_file.txt"])
    r.index.commit("Second version")
    r.create_tag("FeatureFreeze")

    yield repo_path

    # Clean up the repo
    shutil.rmtree(repo_path)
