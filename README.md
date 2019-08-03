# vinnie the versioner

## Overview

`vinnie` is a small utility to handle [semantic versioning](https://semver.org/)
using only git tags.  This can be done either manually or as part of CI.

## Usage

Calling `vinnie` on it's own prints the help.

`vinnie version` prints the current version.

`vinnie patch` increments the patch level, creates the tag, and pushes it.
`vinnie minor` increments the minor number, creates the tag, and pushes it.
`vinnie patch` increments the major number, creates the tag, and pushes it.

`vinnie next (patch|minor|major)` determines the _next_ version number of the
given level and prints it to stdout.

## TODO

- [x] pytest setup
- [x] Environment variables
    - VINNIE_SSH_KEY (for using ssh key with git)
    - VINNIE_GITHUB_TOKEN
    - VINNIE_GITLAB_TOKEN
    - VINNIE_S3_ACCESS_KEY (for validate)
    - VINNIE_S3_SECRET_KEY (for validate)
    - VINNIE_S3_URL (for validate)
    - Repeat these for GCS
    - VINNIE_TAG_PREFIX (for example 'v')
    - VINNIE_SEMVER=False would set it to just do incrementing ints (v1, v2, v3, etc)
- [x] `vinnie` prints help
- [x] `vinnie patch` patches
- [x] `vinnie minor` increments minor revision
- [x] `vinnie major` increments major number
- [x] `vinnie next (patch|minor|major)` returns next version without tagging
- [x] `vinnie version` returns current version, for use in scripts
    - `export IMAGE_TAG=$(vinnie version)`
- [ ] Fix `tests/conftest.py`'s `repo` fixture to build a repo with commits and
      tags to test against
- [ ] `vinnie validate` checks that tags haven't moved
- [ ] Some way to replace version placeholders in files
- [ ] Maybe some way to actually change the files?

## License

BSD Licensed

## Author

[Frank Wiles](https://www.revsys.com) <frank@revsys.com>