# Change Log

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Added feature A.
- Added feature B.

### Changed

- Changed behavior of C.
- Optimized performance of D.

### Removed

- Removed feature E.

### Fixed

- Fixed issue F.

## [0.3.0] - 2023-04-12

### Added

- IPFS folder uploads
- IPFS folder downloads
- With Replace parameter, user can replace the file with the same name.

### Changed

- Changed package name from mcs -> swan_mcs
- list_buckets function now returns a list of Bucket objects or None if error occurs. (Was False before)
- list files function now returns a list of File objects or None if error occurs. (Was False before)
- upload_file function now returns a File object or None if error occurs. (Was False before)
- upload_folder function now returns a list of File objects or None if error occurs. (Was an empty list before)
- delete_file function now returns True if successful or False if error occurs. (Was None before)
- create_folder function now returns True if successful or False if error occurs. (Was None before)

### Removed

### Fixed
- Help user to create Hierarchical Relationships base on the object name so user can see the Hierarchical Relationships
  in the MCS web console.

[Unreleased]: https://github.com/your-project/compare/v1.0.0...HEAD

[0.3.0]: https://github.com/filswan/python-mcs-sdk/releases/tag/v0.3.0

