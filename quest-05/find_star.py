# The librarian wrote this script many years ago, for starmap 1.4.
# It finds a star in the catalog, and prints what the star whispers.
import starmap

catalog = starmap.load("sky.catalog")
star = catalog.search("Vela")
print(star.name, "whispers:", star.whisper)
