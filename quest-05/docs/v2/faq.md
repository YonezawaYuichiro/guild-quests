# FAQ (starmap 2.1)

## Moving from 1.x

starmap 2.0 changed some names. Update your code like this:

| 1.x | 2.x |
| --- | --- |
| `starmap.load(path)` | `starmap.open_catalog(path)` |
| `catalog.search(name)` | `catalog.find(name)` |
| `star.whisper` | `star.whisper()` |

## I get `CatalogError: ... unknown format`. Why?

The catalog file may be old. Files made by starmap 1.x use **format 1**,
but `open_catalog()` reads format 2 by default.
Open an old file with the `format` parameter. See the [API Reference](api.md).

You can see the format in the first line of the file.
A format 1 file starts with `STARMAP CATALOG 1`.

## My code prints `<bound method Star.whisper of ...>`. Why?

You forgot the `()`. In 2.x, `whisper` is a method. See [Moving from 1.x](#moving-from-1x).

## Which stars are in a catalog?

Use `catalog.names()`.
