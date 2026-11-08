# Quest 4: The Voice of the Oracle

The Oracle has a new tool: a **telescope**. With it, the Oracle can read the sky.

"I made the telescope last night," says Mira. "It works well. But look at this."
She runs `python telescope.py --help`. The help shows the options, but no words at all.

"Nobody can use a tool without help. You read the Oracle's help in the last quest.
Now you know what good help looks like. Can you write it for the telescope?"

In the last quest, you **read** help messages.
In this quest, you **write** them.

## Usage

Try the telescope, and look at its help:

    python telescope.py moon
    python telescope.py --help

Write the help texts in `telescope.py`, and check them:

    python check.py --part 1

When a part passes, the checker gives you a word. Answer the stage with it:

    python quest.py --stage 1

There are four parts. Do them in order.

## Files

| File | What it is |
| --- | --- |
| `telescope.py` | The Oracle's telescope. **You edit the help texts in `build_parser()`.** |
| `check.py` | Checks your help texts and gives you a word. |

In `telescope.py`, edit only the texts in `help=""`, `description=""` and `epilog=""`.
Do not change the names, the defaults, or the other code. Do not edit `check.py`.

## How to write a help text

The help of an option says **what the option does**, or **what the user gives**.
Command-line tools usually write it like this:

1. **Start with a small letter.** `show more stars`, not `Show more stars`.
   (Short forms like `RGB` or `UTC` are OK.)
2. **Do not put a `.` at the end.**
3. **Keep it short.** One line, 60 characters or less.
4. **Do not just say the name again.** For `--zoom`, `zoom` tells the user nothing.
   `how many times bigger the sky looks` is better.

Compare:

| Not helpful | Helpful |
| --- | --- |
| `help="Speed."` | `help="how fast the dragon flies, in km per hour"` |
| `help="the color option"` | `help="color of the text on the screen"` |

## Showing the default

Many options have a **default value**: the value that the tool uses when the user does not choose one.
Do not write the value by hand. If someone changes the default later, your help will be wrong.
Write `%(default)s`. argparse puts the real value there:

    parser.add_argument("--speed", type=int, default=30,
                        help="how fast the dragon flies (default: %(default)s)")

`--help` shows:

      --speed SPEED  how fast the dragon flies (default: 30)

Because `%` has this special meaning, a single `%` breaks the help.
To show a `%` sign, write `%%`:

    help="stop when the battery is under 20%%"

## The description and the epilog

The **description** comes at the top of the help. It says what the whole tool does, in one sentence.
Unlike the option help, it is a full sentence: start with a capital letter, and end with a `.`.

The **epilog** comes at the end of the help. Here you can show examples.
A good example is a real command that the user can copy and run:

    epilog="""\
    Examples:
      python dragon.py fly --speed 50
      python dragon.py sleep
    """

## Part 1: Fill the empty help

Every argument of the telescope has an empty help: `help=""`.
Write a help text for each of them. Run the telescope to see what each option does.

    python check.py --part 1

## Part 2: Show the defaults

Some options have a default value. Show it with `%(default)s`.
The checker also runs `--help` to make sure that it works.

    python check.py --part 2

## Part 3: The description and the examples

Write the `description` (one sentence) and the `epilog` with at least one example.
The checker runs your examples. If an example does not work, the checker tells you.

    python check.py --part 3

## Part 4: Your team's game

Your game needs help, too. When the player types `help`, the game shows what they can type.

1. In your game's `main.py`, put the commands in one dictionary called `COMMANDS`.
   The key is the command, and the value is its help text.
   Write **at least three** commands, and include `help` and `quit`.
   Write the help texts in the same way as Part 1.

       COMMANDS = {
           "go <direction>": "move to the next room, like 'go north'",
           ...
       }

2. Use `COMMANDS` in the game. For example, when the player types `help`:

       for command, text in COMMANDS.items():
           print(f"  {command:<16} {text}")

3. Commit and push your change to your team's repository on GitHub.
4. Check your game. Use your team's repository name:

       python check.py --part 4 YOUR-ID/YOUR-GAME

   You can also give a path to your `main.py` on your computer.

Your team works on the same `main.py`. Talk with your team before you edit it.

## Troubleshooting

**`python` is not found**

On macOS, try `python3` instead of `python`.

**`telescope.py has a syntax error`**

Check the quotes and commas around your text. Each text needs `"` at the start and at the end.

**`badly formed help string`, or `--help stops with an error`**

You wrote a single `%` in a help text. Write `%%` instead. `%(default)s` is OK.

**The example in my epilog does not work**

Run the example yourself, and read the error message. Copy the command exactly as you run it.

**`Cannot find the repository`**

Check the name. It is the part after `https://github.com/`, like `mira/dragon-game`.
Your repository must be public.

## Maintainers

This quest is maintained by **Mira**.
If you find a bug in this quest, please open an issue.
See [CONTRIBUTING.md](../CONTRIBUTING.md) to learn how.

## License

This quest is released under the MIT License. See [LICENSE](../LICENSE).
