# API Reference (starmap 2.1)

## `starmap.open_catalog(path, *, format=2)`

Open a catalog file.

**Parameters**

- `path` (str): the path to the catalog file.
- `format` (int, optional): the format version of the file. Default: `2`.
  Use `1` for files made by starmap 1.x.
  This is a keyword-only argument: write `format=1`, not just `1`.

**Returns** a `Catalog`.

**Raises** `CatalogError` if the file is not found, or if it is not in the given format.

*Added in version 2.0.*
*Changed in version 2.1: added the `format` parameter. Before 2.1, only format 2 files could be opened.*

## `Catalog.find(name)`

Find a star by its name. Upper and lower case do not matter.

**Parameters**

- `name` (str): the name of the star.

**Returns** a `Star`.

**Raises** `CatalogError` if the star is not in the catalog.

*Changed in version 2.0: renamed from `search()`. It raises `CatalogError` instead of returning `None`.*

## `Catalog.names()`

**Returns** a list of the names of all stars in the catalog.

*Added in version 2.0.*

## `Star`

**Attributes**

- `name` (str): the name of the star.

**Methods**

- `whisper()`: returns the word that the star whispers (str).

*Changed in version 2.0: `whisper` is now a method. In 1.x, it was an attribute.
Write `star.whisper()`, not `star.whisper`.*

## `CatalogError`

The exception that starmap raises when something goes wrong.

## Removed

- `starmap.load(path)`: *Removed in version 2.0.* Use `open_catalog()`.
