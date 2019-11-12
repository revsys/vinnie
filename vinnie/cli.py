import click
import os

from git.exc import CommandError as GitCommandError

from .base import Vinnie


@click.group(invoke_without_command=True)
@click.option("--push/--no-push", envvar="VINNIE_PUSH", default=True)
@click.option("--repo", envvar="VINNIE_REPO_PATH", default=".")
@click.option("--repo-url", envvar="VINNIE_REPO_URL", default=None)
@click.option("--ssh-key", envvar="VINNIE_SSH_KEY", default=None)
@click.option("--github-token", envvar="VINNIE_GITHUB_TOKEN", default=None)
@click.option("--gitlab-token", envvar="VINNIE_GITLAB_TOKEN", default=None)
@click.option("--prefix", envvar="VINNIE_TAG_PREFIX", default="")
@click.option("--omit-prefix", envvar="VINNIE_OMIT_PREFIX", default=False, is_flag=True)
@click.option("--semver", envvar="VINNIE_SEMVER", default=True)
@click.option("--s3-access-key", envvar="VINNIE_S3_ACCESS_KEY", default=None)
@click.option("--s3-secret-key", envvar="VINNIE_S3_SECRET_KEY", default=None)
@click.option("--s3-url", envvar="VINNIE_S3_URL", default=None)
@click.option("--current-version", envvar="VINNIE_CURRENT_VERSION", default=None)
@click.option("--remote", envvar="VINNIE_GIT_REMOTE", default=None)
@click.option("--marker", envvar="VINNIE_VERSION_MARKER", default="__VINNIE_VERSION__")
@click.pass_context
def cli(ctx, **kwargs):
    """ Vinnie the Versioner """
    ctx.obj = Vinnie(**kwargs)

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit()


@cli.command()
@click.pass_obj
@click.pass_context
def bump(ctx, v):
    """ Bump incrementing integer version """
    try:
        new_value = v.next_bump()
        new_value = v.omit_prefix(new_value)
        click.echo(new_value)
    except ValueError:
        click.echo("version was not an integer; could not bump.")
        ctx.exit(1)


@cli.command()
@click.pass_obj
@click.pass_context
def patch(ctx, v):
    """ Patch version number, tag and push"""
    try:
        new_value = v.next_patch()
        new_value = v.omit_prefix(new_value)
        click.echo(new_value)
    except GitCommandError as e:
        click.echo(str(e))
        ctx.exit(1)


@cli.command()
@click.pass_obj
@click.pass_context
def minor(ctx, v):
    """ Increase minor version, tag and push """
    try:
        new_value = v.next_minor()
        new_value = v.omit_prefix(new_value)
        click.echo(new_value)
    except GitCommandError as e:
        click.echo(str(e))
        ctx.exit(1)


@cli.command()
@click.pass_obj
@click.pass_context
def major(ctx, v):
    """ Increase major version, tag and push """
    try:
        new_value = v.next_major()
        new_value = v.omit_prefix(new_value)
        click.echo(new_value)
    except GitCommandError as e:
        click.echo(str(e))
        ctx.exit(1)


@cli.command()
@click.argument("part")
@click.pass_obj
@click.pass_context
def next(ctx, v, part):
    """ Return next version updating the given part (patch, minor, or major)"""
    try:
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
        next_value = v.omit_prefix(next_value)
        click.echo(next_value)
    except RuntimeError as e:
        click.echo(str(e))
        ctx.exit(1)



@cli.command()
@click.pass_obj
def version(v):
    """ Print current version to stdout """
    version = v.version()
    version = v.omit_prefix(version)
    click.echo(version)


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
    version = v.omit_prefix(version)

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
