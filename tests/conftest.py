import os
import shutil
import pytest

from git import Repo


@pytest.fixture
def repo():
    current_dir = os.path.dirname(__file__)
    repo_path = os.path.join(current_dir, "repo")
    file_path = os.path.join(current_dir, "files")

    r = Repo.init(repo_path, bare=True)
    r.create_head("master")

    shutil.copy(
        os.path.join(file_path, "README.md"), os.path.join(repo_path, "README.md")
    )
    r.index.add(["README.md"])
    r.create_tag("v0.0.1")
    r.index.commit("First version")

    shutil.copy(
        os.path.join(file_path, "another_file.txt"),
        os.path.join(repo_path, "another_file.txt"),
    )
    r.index.add(["another_file.txt"])
    r.create_tag("v0.0.2")
    r.index.commit("Second version")
    yield repo_path

    # Clean up the repo
    shutil.rmtree(repo_path)
