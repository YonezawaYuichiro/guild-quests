# Quickstart (starmap 1.4)

> **Note:** This is the documentation for starmap **1.4**.
> For the latest version, see [the 2.x documentation](../v2/quickstart.md).

Open a catalog, find a star, and read what it whispers:

```python
import starmap

catalog = starmap.load("sky.catalog")
star = catalog.search("Vela")
print(star.whisper)
```

See the [API Reference](api.md) for more.
