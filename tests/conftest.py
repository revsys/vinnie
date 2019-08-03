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
