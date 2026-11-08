"""The telescope of the Oracle. It works, but its help is empty.

  python telescope.py moon --zoom 20

You edit the help texts in build_parser(). Do not change anything else.
"""
import argparse
import sys

TARGETS = ["moon", "stars", "comet"]
FILTERS = ["clear", "red", "blue"]


def build_parser():
    parser = argparse.ArgumentParser(
        prog="telescope.py",
        description="",
        epilog="",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("target", choices=TARGETS,
                        help="")
    parser.add_argument("--zoom", type=int, default=10, metavar="N",
                        help="")
    parser.add_argument("--filter", choices=FILTERS, default="clear",
                        help="")
    parser.add_argument("--hours", type=float, default=2.0,
                        help="")
    parser.add_argument("--clouds", type=int, default=50, metavar="PERCENT",
                        help="")
    parser.add_argument("--save", metavar="FILE",
                        help="")
    parser.add_argument("--quiet", action="store_true",
                        help="")
    return parser


def observe(args):
    lines = [f"You point the telescope at the {args.target}.",
             f"Zoom: x{args.zoom}. Filter: {args.filter}. You watch for {args.hours:g} hours.",
             f"If clouds cover more than {args.clouds}% of the sky, you stop."]
    if args.target == "comet":
        lines.append("A comet with a long blue tail flies across the sky.")
    else:
        lines.append(f"The {args.target} shines quietly.")
    return lines


def main():
    args = build_parser().parse_args()
    lines = observe(args)
    if not args.quiet:
        print("\n".join(lines))
    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"Saved to {args.save}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
