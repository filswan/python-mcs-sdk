# Change Log

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added


### Changed


### Removed


### Fixed


## [0.3.1] - 2023-04-12

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
  
[0.3.1]: https://github.com/filswan/python-mcs-sdk/releases/tag/v0.3.1
[Unreleased]: https://github.com/filswan/python-mcs-sdk/tree/dev
