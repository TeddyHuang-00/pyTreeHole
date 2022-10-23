# Changelog

## Version 0.0.1

- Add basic functionality
- Remove redundant documentation files

## Version 0.0.2

- Fix broken dependencies problem

## Version 0.0.3

- Move `GenericHole` type to models, you can now use it in your own functions
- Add `get_hole_image` method to `Client`, which returns the hole image as a bytes string and the content type
- Rename `search` method to `get_search` for consistency
  - **Since we're still in development, this becomes a patch rather than a minor version**
- Add a new data model for user nicknames
- Add a bunch of `post_*` methods to client! You can now post comments, holes, attentions!
- Rename `test-client.py` to `test-get.py`
