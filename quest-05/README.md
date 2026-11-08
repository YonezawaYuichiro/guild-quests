# Quest 5: The Great Library

The Oracle gave you a clue: "Go to the **Great Library**. The stars will tell you the rest."

The Great Library is the biggest room in the Guild. Mira opens the heavy door.

"Everything is written down here," says Mira. "But a library is only useful
if you can find the right page. Developers do this every day:
they read the **official documentation**."

In this quest, you read **documentation**: first Python's own, and then the documentation of a library.

## Usage

Answer the stages:

    python quest.py --stage 1
    python quest.py --stage 2
    python quest.py --stage 3
    python quest.py --stage 4
    python quest.py --stage 5

## Files

| File | What it is |
| --- | --- |
| `find_star.py` | An old script by the librarian. It uses the `starmap` library (stages 4 and 5). |
| `starmap/` | The `starmap` library. |
| `docs/` | The documentation of `starmap`. Start with `docs/index.md`. |
| `sky.catalog` | A star catalog. |
| `old.catalog` | A very old star catalog. |

You may edit `find_star.py`, and create new files in this folder.
Do not edit the `starmap` library or the catalogs.

## Part 1: Python's documentation (stages 1 to 3)

The official Python documentation is at https://docs.python.org/3/

Two parts of it are very useful:

| Page | What is in it |
| --- | --- |
| [The Python Standard Library](https://docs.python.org/3/library/index.html) | Every module that comes with Python, like `math`, `random` and `json`. |
| [Built-in Types](https://docs.python.org/3/library/stdtypes.html) | `str`, `list`, `dict`, and their methods. |

To find something on a long page, use your browser's search (`Ctrl+F`, or `Cmd+F` on macOS).

### How to read an entry

Each function has an **entry** like this:

> **round(number, ndigits=None)**
>
> Return *number* rounded to *ndigits* precision after the decimal point.
> If *ndigits* is omitted or is `None`, it returns the nearest integer to its input.

- The first line is the **signature**: the name of the function and its **parameters**.
- `ndigits=None` means that `ndigits` has a default value. You can leave it out.
- A `/` in the signature means: the parameters before it cannot be given by name.
- Some entries end with a note about versions:

| Note | It means |
| --- | --- |
| *Added in version X* | It does not exist in versions before X. |
| *Changed in version X* | It works differently from version X. |
| *Deprecated since version X* | It still works, but it will be removed. Stop using it. |

Older pages may say *New in version X* instead of *Added in version X*. They mean the same thing.

## Part 2: The library's documentation (stages 4 and 5)

The librarian wrote `find_star.py` many years ago. It does not work anymore:

    python find_star.py

Libraries change. When a new version comes out, some functions get new names,
and some are removed. So the first question is always:
**Which version do I have, and which version is this page for?**

Open `docs/index.md` and start from there.

## Troubleshooting

**`python` is not found**

On macOS, try `python3` instead of `python`.

**`ModuleNotFoundError: No module named 'starmap'`**

Run `find_star.py` in this folder (the folder that has the `starmap` folder in it).

**The documentation page looks different from the example above**

That is OK. The design of the page changes from version to version.
The signature and the version notes are always there.

## Maintainers

This quest is maintained by **Mira**.
If you find a bug in this quest, please open an issue.
See [CONTRIBUTING.md](../CONTRIBUTING.md) to learn how.

## License

This quest is released under the MIT License. See [LICENSE](../LICENSE).
