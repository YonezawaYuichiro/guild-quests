"""Checks the help texts, and gives you a word when they pass.

  python check.py --part 1
  python check.py --part 2
  python check.py --part 3
  python check.py --part 4 YOUR-ID/YOUR-GAME     (or a path to your main.py)

This checker can only check the form of a help text, not how good it is.
Read your help aloud, and ask yourself: "Would this help a new user?"
"""
import argparse
import ast
import base64
import contextlib
import importlib.util
import io
import os
import re
import shlex
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_LENGTH = 60
# Words that do not explain anything by themselves.
EMPTY_WORDS = {"a", "an", "the", "of", "to", "for", "in", "on", "at", "is", "it", "this", "that", "and", "or",
               "option", "value", "argument", "set", "sets", "use", "uses", "default", "flag", "command"}
WORDS = {1: "Y2xhcml0eQ==", 2: "aG9yaXpvbg==", 3: "YmVhY29u", 4: "Y2hvcnVz"}
BAD_PERCENT = "To show a '%' sign in a help text, write '%%'. For example: 'more than 50%% of the sky'."


def name_of(action):
    return "/".join(action.option_strings) or action.dest


def expand(text, params):
    """Show the text as --help shows it, without breaking on a wrong '%'."""
    text = re.sub(r"%\((\w+)\)s", lambda m: str(params.get(m.group(1), m.group(0))), text)
    return text.replace("%%", "%")


def help_problems(text, names, params=None):
    """Part 1 rules: the help is there, short, and written like other command-line tools."""
    if not text or not text.strip():
        return ["The help is empty. Write what it does."]
    problems = []
    shown = expand(text, params or {})
    first = re.match(r"[A-Za-z0-9]+", shown)
    if not first or (shown[0].isupper() and not re.fullmatch(r"[A-Z0-9]{2,}s?", first.group())):
        problems.append("Start with a small letter, like 'show' or 'how many'. (Short forms like 'RGB' are OK.)")
    if shown.rstrip().endswith("."):
        problems.append("Do not put a '.' at the end. Most tools write help without it.")
    if len(shown) > MAX_LENGTH:
        problems.append(f"The help is too long ({len(shown)} characters). Keep it to {MAX_LENGTH} or less.")
    words = set(re.findall(r"[a-z]+", re.sub(r"%\(\w+\)s", "", text).lower()))
    own = set(re.findall(r"[a-z]+", " ".join(names).lower()))
    if not words - own - EMPTY_WORDS:
        problems.append("The help only says the name again. Say what it does, or what the user gives.")
    return problems


def load_parser():
    """Run build_parser() from telescope.py, and return the parser."""
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("telescope", HERE / "telescope.py")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except SyntaxError as err:
        sys.exit(f"telescope.py has a syntax error on line {err.lineno}: {err.msg}\n"
                 "Check the quotes ( \" ) and commas ( , ) around your help texts.")
    try:
        return module.build_parser()
    except ValueError as err:
        sys.exit(f"telescope.py stops with an error: {err}\n{BAD_PERCENT}")


def show_help(parser):
    """Return the problem if --help cannot be shown."""
    try:
        parser.format_help()
    except (ValueError, TypeError, KeyError) as err:
        return f"--help stops with an error: {err}\n    {BAD_PERCENT}"
    return None


def check_arguments(parser, part):
    failed = 0
    for action in parser._actions:
        if isinstance(action, argparse._HelpAction):
            continue
        params = dict(vars(action), prog=parser.prog)
        if action.choices is not None:
            params["choices"] = ", ".join(map(str, action.choices))
        names = action.option_strings + [action.dest, action.metavar or ""]
        problems = help_problems(action.help, names, params)
        if part >= 2 and not problems and action.option_strings and action.nargs != 0 \
                and action.default is not None and "%(default)s" not in action.help:
            problems.append(f"This option has a default value ({action.default}). "
                            "Show it with %(default)s, like '(default: %(default)s)'.")
        if problems:
            failed += 1
            print(f"[{name_of(action)}] {action.help!r}")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"[{name_of(action)}] OK")
    return failed


def description_problems(text):
    if not text or not text.strip():
        return ["The description is empty. Write one sentence about the tool."]
    problems = []
    text = text.strip()
    if not text[0].isupper():
        problems.append("Start the description with a capital letter.")
    if not text.endswith("."):
        problems.append("End the description with a '.'.")
    if len(re.findall(r"[.!?](?:\s|$)", text)) > 1 or "\n" in text:
        problems.append("Write only one sentence. Put examples and notes in the epilog.")
    return problems


def example_problems(parser, text):
    lines = [re.sub(r"^\$\s*", "", line.strip()) for line in (text or "").splitlines()]
    examples = [line for line in lines if re.match(r"python3? telescope\.py(\s|$)", line)]
    if not examples:
        return ["Write at least one example in the epilog, like: python telescope.py moon --zoom 20"]
    problems = []
    for line in examples:
        try:
            args = shlex.split(line)[2:]
        except ValueError as err:
            problems.append(f"'{line}': {err}")
            continue
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                parser.parse_args(args)
        except SystemExit as exit_:
            if exit_.code == 0:
                problems.append(f"'{line}': show a real command, not the help.")
            else:
                error = out.getvalue().strip().splitlines()[-1:] or ["error"]
                problems.append(f"'{line}' does not work:\n        {error[0]}")
            continue
        print(f"[example] {line}  OK")
    return problems


def check_telescope(part):
    parser = load_parser()
    failed = check_arguments(parser, part)
    if part >= 2:
        problem = show_help(parser)
        if problem:
            print(f"[--help] {problem}")
            failed += 1
    if part >= 3:
        for title, problems in (("description", description_problems(parser.description)),
                                ("epilog", example_problems(parser, parser.epilog))):
            if problems:
                failed += 1
                print(f"[{title}] {(getattr(parser, title) or '').strip()!r}")
                for p in problems:
                    print(f"    - {p}")
            else:
                print(f"[{title}] OK")
    return failed


def fetch_game(target):
    """Read main.py from a local path, or from a public GitHub repository (OWNER/REPO)."""
    path = Path(target)
    if path.is_dir():
        path = path / "main.py"
    if path.is_file():
        return path.read_text(encoding="utf-8")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", target):
        sys.exit(f"'{target}' is not a file. Give a path to main.py, or YOUR-ID/YOUR-GAME.")
    url = f"https://github.com/{target}.git"
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    result = subprocess.run(["git", "ls-remote", url, "HEAD"], capture_output=True, text=True,
                            env=env, stdin=subprocess.DEVNULL, timeout=30)
    if result.returncode != 0 or not result.stdout:
        sys.exit(f"Cannot find the repository {url}\nCheck the name. Is the repository public?")
    sha = result.stdout.split()[0]
    try:
        with urllib.request.urlopen(f"https://raw.githubusercontent.com/{target}/{sha}/main.py", timeout=20) as r:
            return r.read().decode("utf-8")
    except OSError as err:
        sys.exit(f"Cannot read main.py from {target}: {err}\n"
                 "Is main.py at the top of the repository? Did you push it?")


def game_commands(source):
    """Find COMMANDS = {"command": "help", ...} in the game, and check that the game uses it."""
    try:
        tree = ast.parse(source)
    except SyntaxError as err:
        sys.exit(f"main.py has a syntax error on line {err.lineno}: {err.msg}")
    found = None
    used = False
    for node in ast.walk(tree):
        target = node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else getattr(node, "target", None)
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(target, ast.Name) and target.id == "COMMANDS":
            try:
                found = ast.literal_eval(node.value)
            except ValueError:
                sys.exit("COMMANDS must be a plain dictionary of strings, like {\"look\": \"...\"}.")
        if isinstance(node, ast.Name) and node.id == "COMMANDS" and isinstance(node.ctx, ast.Load):
            used = True
    if not isinstance(found, dict):
        sys.exit("Cannot find COMMANDS = {...} in main.py. See 'Part 4' in README.md.")
    if not used:
        sys.exit("COMMANDS is written, but the game does not use it yet. Show it when the player types 'help'.")
    return found


def check_game(commands):
    failed = 0
    for key, text in commands.items():
        if not isinstance(key, str) or not isinstance(text, str):
            print(f"[{key!r}] Write the command and its help as strings, like \"look\": \"...\".")
            failed += 1
            continue
        problems = help_problems(text, [key])
        if problems:
            failed += 1
            print(f"[{key}] {text!r}")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"[{key}] OK")
    first_words = {key.split()[0].lower() for key in commands if isinstance(key, str) and key.split()}
    for needed in ("help", "quit"):
        if needed not in first_words:
            print(f"COMMANDS has no '{needed}'. Every game needs it.")
            failed += 1
    if len(commands) < 3:
        print(f"COMMANDS has {len(commands)} command(s). Write at least 3.")
        failed += 1
    return failed


def main():
    parser = argparse.ArgumentParser(description="Check help texts.",
                                     epilog="Example: python check.py --part 4 your-id/your-game")
    parser.add_argument("--part", type=int, choices=[1, 2, 3, 4], required=True, help="which part to check")
    parser.add_argument("game", nargs="?", help="part 4 only: YOUR-ID/YOUR-GAME, or a path to main.py")
    args = parser.parse_args()

    if args.part < 4:
        failed = check_telescope(args.part)
    else:
        if not args.game:
            parser.error("part 4 needs your game: python check.py --part 4 YOUR-ID/YOUR-GAME")
        failed = check_game(game_commands(fetch_game(args.game)))

    print()
    if failed:
        print("Not yet. Fix the problems above, and run the checker again.")
        return 1
    print(f"Part {args.part} passed!")
    print(f"The word for stage {args.part} is: {base64.b64decode(WORDS[args.part]).decode()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
