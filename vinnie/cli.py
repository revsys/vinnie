import click
import os

from .base import Vinnie


@click.group(invoke_without_command=True)
@click.option("--repo", envvar="VINNIE_REPO_PATH", default=".")
@click.option("--repo-url", envvar="VINNIE_REPO_URL", default=None)
@click.option("--ssh-key", envvar="VINNIE_SSH_KEY", default=None)
@click.option("--github-token", envvar="VINNIE_GITHUB_TOKEN", default=None)
@click.option("--gitlab-token", envvar="VINNIE_GITLAB_TOKEN", default=None)
@click.option("--prefix", envvar="VINNIE_TAG_PREFIX", default="")
@click.option("--semver", envvar="VINNIE_SEMVER", default=True)
@click.option("--s3-access-key", envvar="VINNIE_S3_ACCESS_KEY", default=None)
@click.option("--s3-secret-key", envvar="VINNIE_S3_SECRET_KEY", default=None)
@click.option("--s3-url", envvar="VINNIE_S3_URL", default=None)
@click.option("--current-version", envvar="VINNIE_CURRENT_VERSION", default=None)
@click.option("--remote", envvar="VINNIE_GIT_REMOTE", default=None)
@click.option("--marker", envvar="VINNIER_VERSION_MARKER", default="__VINNIE_VERSION__")
@click.pass_context
def cli(ctx, **kwargs):
    """ Vinnie the Versioner """
    ctx.obj = Vinnie(**kwargs)

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit()


@cli.command()
@click.pass_obj
def bump(v):
    """ Bump incrementing integer version """
    new_value = v.next_bump()
    click.echo(new_value)


@cli.command()
@click.pass_obj
def patch(v):
    """ Patch version number, tag and push"""
    new_value = v.next_patch()
    click.echo(new_value)


@cli.command()
@click.pass_obj
def minor(v):
    """ Increase minor version, tag and push """
    new_value = v.next_minor()
    click.echo(new_value)


@cli.command()
@click.pass_obj
def major(v):
    """ Increase major version, tag and push """
    new_value = v.next_major()
    click.echo(new_value)


@cli.command()
@click.argument("part")
@click.pass_obj
def next(v, part):
    """ Return next version updating the given part (patch, minor, or major)"""
    if part == "patch":
        next_value = v.get_next_patch()
    elif part == "minor":
        next_value = v.get_next_minor()
    elif part == "major":
        next_value = v.get_next_major()
    else:
        raise RuntimeError(
            f"Unknown next value '{part}'. Must be patch, minor, or major"
        )

    click.echo(next_value)


@cli.command()
@click.pass_obj
def version(v):
    """ Print current version to stdout """
    v = v.version()
    click.echo(v)


@cli.command()
@click.pass_obj
def validate(v):
    """
    TODO - Store tag/sha combos in a file (local, S3, GCS) to validate that no
    tags have moved since the last run. Store new tags
    """
    raise NotImplementedError("This feature is not implemented yet.")


@cli.command()
@click.argument(
    "filename",
    type=click.Path(exists=True, dir_okay=False, writable=True, resolve_path=True),
)
@click.pass_obj
def replace(v, filename):
    """ Replace placeholder with current version """
    version = v.version()

    temp_filename = f"{filename}.tmp"
    f = open(temp_filename, "w+")
    r = open(filename)

    for line in r:
        if v.config.marker in line:
            line = line.replace(v.config.marker, version)
        f.write(line)

    r.close()
    f.close()
    os.rename(temp_filename, filename)


@cli.command()
@click.pass_obj
def show_config(v):
    """ Show the current configuration """
    v.dump()
