# API Reference (starmap 1.4)

> **Note:** This is the documentation for starmap **1.4**.
> For the latest version, see [the 2.x documentation](../v2/api.md).

## `starmap.load(path)`

Open a catalog file.

**Parameters**

- `path` (str): the path to the catalog file.

**Returns** a `Catalog`.

## `Catalog.search(name)`

Find a star by its name.

**Parameters**

- `name` (str): the name of the star.

**Returns** a `Star`, or `None` if the star is not in the catalog.

## `Star`

**Attributes**

- `name` (str): the name of the star.
- `whisper` (str): the word that the star whispers.
