# vinnie the versioner

## Overview

`vinnie` is a small utility to handle [semantic versioning](https://semver.org/)
using only git tags.  This can be done either manually or as part of CI.

## Usage

## TODO

- [ ] pytest setup
- [ ] Environment variables
    - VINNIE_SSH_KEY (for using ssh key with git)
    - VINNIE_GITHUB_TOKEN
    - VINNIE_GITLAB_TOKEN
    - VINNIE_S3_ACCESS_KEY (for validate)
    - VINNIE_S3_SECRET_KEY (for validate)
    - VINNIE_S3_URL (for validate)
    - Repeat these for GCS
    - VINNIE_TAG_PREFIX (for example 'v')
    - VINNIE_SEMVER=False would set it to just do incrementing ints (v1, v2, v3, etc)
- [ ] `vinnie` prints help
- [ ] `vinnie patch` patches
- [ ] `vinnie minor` increments minor revision
- [ ] `vinnie major` increments major number
- [ ] `vinnie next (patch|minor|major)` returns next version without tagging
- [ ] `vinnie version` returns current version, for use in scripts
    - `export IMAGE_TAG=$(vinnie version)`
- [ ] `vinnie validate` checks that tags haven't moved
- [ ] Some way to replace version placeholders in files
- [ ] Maybe some way to actually change the files?

## License

BSD Licensed

## Author

[Frank Wiles](https://www.revsys.com) <frank@revsys.com>