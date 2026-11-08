# Quickstart (starmap 2.1)

Open a catalog, find a star, and read what it whispers:

```python
import starmap

catalog = starmap.open_catalog("sky.catalog")
star = catalog.find("Vela")
print(star.whisper())
```

Are you moving from starmap 1.x? Read [Moving from 1.x](faq.md#moving-from-1x) first.

See the [API Reference](api.md) for more.
