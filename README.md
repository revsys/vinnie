# vinnie the versioner

## Overview

`vinnie` is a small utility to handle [semantic versioning](https://semver.org/)
using only git tags.  This can be done either manually or as part of CI.

## Motivation

The motivation was building vinnie is somewhat small and trivial. Many existing
tools force you to keep the "current version" in a file in your git repository
which often means that during a CI build process you generate a commit that
is simply incrementing the version number.  By no means is this the end of the
world, but we realized we could fairly safely just use git tags as the storage
mechanism for the current version.

## Usage

Calling `vinnie` on it's own prints the help.

`vinnie version` prints the current version to stdout.

`vinnie (patch|minor|major)` increments the version number of the given level, creates the tag, and pushes it.

`vinnie next (patch|minor|major)` determines the _next_ version number of the
given level and prints it to stdout.

`vinnie replace /path/to/file` will replace the marker (default of `__VINNIE_VERSION__`)
in this file with the current version.

`vinnie show-config` dumps the current configuration vinnie is operating with,
mostly for debugging.

## Non semantic versioning

Vinnie also supports not using [semver](https://semver.org/) by just using an
incrementing integer (v1, v2, ... v47) if you with.  To do that you need to
always pass in the option `--semver=False` and then the only incrementing
command to use is bump.

```shell
$ vinnie --semver=False bump
```

## Options

`--repo` set the filesystem path to the root of the git checkout

`--repo-url` set the URL on a supported provider for the repository

`--ssh-key` path to the ssh key to use on disk

`--github-token` Github API token

`--gitlab-token` Gitlab API token

`--prefix` allows you to set an optional text prefix to all version numbers for
example, `vinnie --prefix=v` would create version numbers such as `v0.0.1`.

`--semver` sets whether or not you want to use semantic versioning or just an
incrementing integer. The default is to use semver.

`--current-version` in some situations it's nice to be able to just tell vinnie
what the current version is, this option allows you to do that.  In this case,
vinnie ignores whatever versions actually exist as tags on the repository.

## Environment Variables

Vinnie also listens for environment variables if you would prefer to use those
the following map to the given option

- `VINNIE_REPO_PATH` sets `--repo`
- `VINNIE_REPO_URL` sets `--repo-url`
- `VINNIE_SSH_KEY` sets `--ssh-key`
- `VINNIE_GITHUB_TOKEN` sets `--github-token`
- `VINNIE_GITLAB_TOKEN` sets `--gitlab-token`
- `VINNIE_PREFIX` sets `--prefix`
- `VINNIE_SEMVER` sets `--semver`
- `VINNIE_S3_ACCESS_KEY` sets `--s3-access-key`
- `VINNIE_S3_SECRET_KEY` sets `--s3-secret-key`
- `VINNIE_S3_URL` sets `--s3-url`
- `VINNIE_CURRENT_VERSION` sets `--current-version`
- `VINNIE_REMOTE` sets `--remote`
- `VINNIE_MARKER` sets `--marker`

## Examples

Let's start off with a simple example:

```shell
$ cd my-git-repo
$ vinnie version
0.0.0
$ vinnie patch
0.0.1
```

Or maybe you want to use a prefix on with a project that already has been
using semver in a pattern of `vX.Y.Z` in tags, you would then just need to do:

```shell
$ cd my-git-repo
$ vinnie --prefix=v version
v1.2.3
$ vinnie --prefix=v minor
v1.3.0
```

## Similar Projects

Vinnie is very similar to these other fine projects:

- [bumpversion](https://pypi.org/project/bumpversion/)
- [semver (js)](https://www.npmjs.com/package/semver)
- [semver (python)](https://pypi.org/project/semver/)

## Roadmap / TODO

- [ ] `vinnie validate` checks that tags haven't moved
- [ ] Support storing the validation file in S3
- [ ] Support storing the validation file in GCS
- [ ] Support versioning without SSH or the repo with Github API Token
- [ ] Support versioning without SSH or the repo with Gitlab API Token

## License

BSD Licensed

## Author

Originally written by [Frank Wiles](https://frankwiles.com) <frank@revsys.com>
and brought to you by [REVSYS](https://www.revsys.com).

## Keep in touch!

If you have a question about this project, please open a GitHub issue. If you love us and want to keep track of our goings-on, here's where you can find us online:

<a href="https://revsys.com?utm_medium=github&utm_source=vinnie"><img src="https://pbs.twimg.com/profile_images/915928618840285185/sUdRGIn1_400x400.jpg" height="50" /></a>
<a href="https://twitter.com/revsys"><img src="https://cdn1.iconfinder.com/data/icons/new_twitter_icon/256/bird_twitter_new_simple.png" height="43" /></a>
<a href="https://www.facebook.com/revsysllc/"><img src="https://cdn3.iconfinder.com/data/icons/picons-social/57/06-facebook-512.png" height="50" /></a>
<a href="https://github.com/revsys/"><img src="https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png" height="53" /></a>
<a href="https://gitlab.com/revsys"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/GitLab_Logo.svg/2000px-GitLab_Logo.svg.png" height="44" /></a>