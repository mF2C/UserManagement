# Changelog (User Management)
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.9] - 2019-10-08
### Changed
- UM returns `device_id` when called from LM before deploying a service
- UM assessment interval changed

## [1.3.6] - 2019-08-08
### Changed
- logs and exceptions updated
- errors handling improved

### Fixed
- path updated: GET /um/user/<string:user_id>

## [1.2.8] - 2019-06-17
### Added
- Changelog file added to project
- data adpater for mF2C and standalone modes
- standalone mode implemented

### Changed
- packages structure updated

### Fixed
- deleted user method
