# Changelog

## Version 1.1.2

- Minor patch for unawaited async function
- A new example for async methods usage (see [sample_async.py](./tests/sample_async.py))

## Version 1.1.1

- Minor patch of backwards compatibility for up to Python 3.6! Thank you, [vermin](https://github.com/netromdk/vermin)!

## Version 1.1.0

- Revise redundant code in calls to `requests`
- Asynchronous methods are now available! They come with `_async` suffixes compared to their synchronous counterparts.

## Version 1.0.1

- Minor patch for demo case in README.md

## Version 1.0.0

- Rename `Client` class to `TreeHoleClient` to avoid similar name with submodule `client` (breaks backward compatibility)
- Documentation is out! Check it out at [GitHub Pages](https://teddyhuang-00.github.io/pyTreeHole)
- Refactor code, add more unit tests using [`pytest`](https://docs.pytest.org/en/stable/)

## Version 0.0.3

- Move `GenericHole` type to models, you can now use it in your own functions
- Add `get_hole_image` method to `Client`, which returns the hole image as a bytes string and the content type
- Rename `search` method to `get_search` for consistency
  - **Since we're still in development, this becomes a patch rather than a minor version**
- Add a new data model for user nicknames
- Add a bunch of `post_*` methods to client! You can now post comments, holes, attentions!
- Rename `test-client.py` to `test-get.py`

## Version 0.0.2

- Fix broken dependencies problem

## Version 0.0.1

- Add basic functionality
- Remove redundant documentation files
