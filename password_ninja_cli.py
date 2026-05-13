"""Command-line interface for the Password Ninja API."""

from __future__ import annotations

import argparse
import json
import sys

from password_ninja_api import DEFAULT_API_URL, PasswordNinjaError, PasswordNinjaOptions, generate_passwords


def _add_boolean_flag(parser: argparse.ArgumentParser, name: str, default: bool, help_text: str) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument(f"--{name}", dest=name, action="store_true", help=help_text)
    group.add_argument(f"--no-{name}", dest=name, action="store_false", help=argparse.SUPPRESS)
    parser.set_defaults(**{name: default})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate passwords from the Password Ninja API.")
    parser.add_argument("--base-url", default=DEFAULT_API_URL, help="Password Ninja API endpoint.")
    parser.add_argument("--min-pass-length", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=20)
    parser.add_argument("--num-at-end", type=int, default=2)
    parser.add_argument("--num-of-passwords", type=int, default=1)
    parser.add_argument("--letters-for-numbers", type=int, default=0)
    parser.add_argument("--letters-for-symbols", type=int, default=0)
    parser.add_argument("--exclude-symbols", default="")

    _add_boolean_flag(parser, "animals", True, "Enable the animals word list.")
    _add_boolean_flag(parser, "instruments", False, "Enable the instruments word list.")
    _add_boolean_flag(parser, "colours", False, "Enable the colours word list.")
    _add_boolean_flag(parser, "shapes", False, "Enable the shapes word list.")
    _add_boolean_flag(parser, "food", False, "Enable the food word list.")
    _add_boolean_flag(parser, "sports", False, "Enable the sports word list.")
    _add_boolean_flag(parser, "transport", False, "Enable the transport word list.")
    _add_boolean_flag(parser, "symbols", False, "Add a random symbol to the end.")
    _add_boolean_flag(parser, "capitals", False, "Capitalise the first letter of each word.")
    _add_boolean_flag(parser, "spacers", False, "Add hyphens between words.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--rand-capitals", dest="randCapitals", action="store_true", help="Randomly capitalise letters throughout the password.")
    group.add_argument("--randCapitals", dest="randCapitals", action="store_true", help=argparse.SUPPRESS)
    group.add_argument("--no-rand-capitals", dest="randCapitals", action="store_false", help=argparse.SUPPRESS)
    parser.set_defaults(randCapitals=False)

    parser.add_argument("--json", action="store_true", help="Print JSON instead of one password per line.")
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    options = PasswordNinjaOptions(
        minPassLength=args.min_pass_length,
        maxLength=args.max_length,
        numAtEnd=args.num_at_end,
        numOfPasswords=args.num_of_passwords,
        animals=args.animals,
        instruments=args.instruments,
        colours=args.colours,
        shapes=args.shapes,
        food=args.food,
        sports=args.sports,
        transport=args.transport,
        symbols=args.symbols,
        capitals=args.capitals,
        spacers=args.spacers,
        randCapitals=args.randCapitals,
        lettersForNumbers=args.letters_for_numbers,
        lettersForSymbols=args.letters_for_symbols,
        excludeSymbols=args.exclude_symbols,
    )

    try:
        passwords = generate_passwords(options, base_url=args.base_url)
    except PasswordNinjaError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"count": len(passwords), "passwords": passwords}, indent=2))
        return 0

    print("\n".join(passwords))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
