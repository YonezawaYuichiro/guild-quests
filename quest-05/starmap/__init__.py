"""starmap: read the star catalogs of the Guild.

Do not edit this library. Read its documentation in the docs folder.
"""
import base64
import json
from pathlib import Path

__version__ = "2.1.0"
__all__ = ["CatalogError", "Catalog", "Star", "open_catalog"]

_FORMAT1_HEADER = "STARMAP CATALOG 1"


class CatalogError(Exception):
    """A catalog cannot be read, or a star is not in it."""


class Star:
    def __init__(self, name, secret):
        self.name = name
        self._secret = secret

    def whisper(self):
        """Return the word that the star whispers."""
        return base64.b64decode(self._secret).decode()

    def __repr__(self):
        return f"Star({self.name!r})"


class Catalog:
    def __init__(self, path, stars):
        self.path = path
        self._stars = stars

    def names(self):
        """Return the names of all stars in the catalog."""
        return sorted(self._stars)

    def find(self, name):
        """Return the star called name. Upper and lower case do not matter."""
        for key, secret in self._stars.items():
            if key.lower() == name.strip().lower():
                return Star(key, secret)
        raise CatalogError(f"there is no star called {name!r} in {self.path}")


def _read_format1(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != _FORMAT1_HEADER:
        return None
    stars = {}
    for line in lines[1:]:
        if "|" in line:
            name, secret = line.split("|", 1)
            stars[name.strip()] = secret.strip()
    return stars


def _read_format2(text):
    try:
        data = json.loads(text)
    except ValueError:
        return None
    if not isinstance(data, dict) or data.get("format") != 2:
        return None
    return dict(data.get("stars", {}))


def open_catalog(path, *, format=2):
    """Open a catalog file, and return a Catalog. See docs/v2/api.md."""
    readers = {1: _read_format1, 2: _read_format2}
    if format not in readers:
        raise CatalogError(f"format must be 1 or 2, not {format!r}")
    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CatalogError(f"cannot find the catalog file {path!r}") from None
    stars = readers[format](text)
    if stars is None:
        raise CatalogError(f"cannot read {path!r}: unknown format (expected format {format})")
    return Catalog(str(path), stars)
