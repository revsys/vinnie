from click.testing import CliRunner

from vinnie.cli import cli


def test_help_runs():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_invalid_options():
    runner = CliRunner()
    result = runner.invoke(cli, ["--repo ./foo/", "--repo-url https://github"])
    assert result.exit_code != 0


def test_version(repo):
    runner = CliRunner()
    result = runner.invoke(cli, [f"--repo={repo}", "--prefix=v", "version"])
    assert result.exit_code == 0
    assert result.output == "v0.0.2\n"


def test_next_patch(repo):
    runner = CliRunner()
    result = runner.invoke(cli, [f"--repo={repo}", "--prefix=v", "next", "patch"])
    assert result.exit_code == 0
    assert result.output == "v0.0.3\n"


def test_next_minor(repo):
    runner = CliRunner()
    result = runner.invoke(cli, [f"--repo={repo}", "--prefix=v", "next", "minor"])
    assert result.exit_code == 0
    assert result.output == "v0.1.0\n"


def test_next_major(repo):
    runner = CliRunner()
    result = runner.invoke(cli, [f"--repo={repo}", "--prefix=v", "next", "major"])
    assert result.exit_code == 0
    assert result.output == "v1.0.0\n"


def test_next_invalid(repo):
    runner = CliRunner()
    result = runner.invoke(cli, [f"--repo={repo}", "--prefix=v", "next", "invalid"])
    assert result.exit_code != 0


def test_bump(non_semver_repo):
    runner = CliRunner()
    result = runner.invoke(
        cli, [f"--repo={non_semver_repo}", "--prefix=v", "--semver=False", "bump"]
    )
    assert result.exit_code == 0
    assert result.output == "v3\n"


def test_show_config(repo):
    runner = CliRunner()
    result = runner.invoke(cli, [f"--repo={repo}", "--prefix=v", "show-config"])
    assert result.exit_code == 0
