import argparse
import secrets
import string

VERSION: str = "0.3.0"

DEFAULT_LENGTH: int = 20
MIN_LENGTH: int = 15
MIN_DIGITS: int = 3
AMBIGUOUS_CHARACTERS: str = "0O1lI"

DEFAULT_PASSWORD_COUNT: int = 1
MAX_PASSWORD_COUNT: int = 100

ALPHABET: str = string.ascii_letters + string.digits + string.punctuation


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate cryptographically secure passwords."
    )

    parser.add_argument(
        "--length",
        type=int,
        help=f"Password length (minimum: {MIN_LENGTH}).",
    )

    parser.add_argument(
        "--count",
        type=int,
        help=f"Number of passwords (1-{MAX_PASSWORD_COUNT}).",
    )

    parser.add_argument(
        "--exclude-ambiguous",
        action="store_true",
        help="Exclude ambiguous characters (0, O, 1, l, I).",
    )

    parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help="Exclude lowercase letters.",
    )

    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Exclude uppercase letters.",
    )

    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits.",
    )

    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print passwords only, one per line.",
    )

    args = parser.parse_args(argv)

    if args.length is not None and args.length < MIN_LENGTH:
        parser.error(f"--length must be at least {MIN_LENGTH}.")

    if args.count is not None and not 1 <= args.count <= MAX_PASSWORD_COUNT:
        parser.error(f"--count must be between 1 and {MAX_PASSWORD_COUNT}.")

    if all(
        (
            args.no_lowercase,
            args.no_uppercase,
            args.no_digits,
            args.no_symbols,
        )
    ):
        parser.error("At least one character type must be enabled.")

    return args


def get_password_length() -> int:
    while True:
        user_input: str = input(f"Password length [{DEFAULT_LENGTH}]: ").strip()

        if user_input == "":
            return DEFAULT_LENGTH

        try:
            password_length = int(user_input)
        except ValueError:
            print("Invalid input. Enter a whole number.")
            continue

        if password_length < MIN_LENGTH:
            print(f"Password must be at least {MIN_LENGTH} characters.")
            continue

        return password_length


def get_password_count() -> int:
    while True:
        user_input = input(f"Number of passwords [{DEFAULT_PASSWORD_COUNT}]: ").strip()

        if user_input == "":
            return DEFAULT_PASSWORD_COUNT

        try:
            password_count = int(user_input)
        except ValueError:
            print("Invalid input. Enter a whole number.")
            continue

        if not 1 <= password_count <= MAX_PASSWORD_COUNT:
            print(f"Number of passwords must be between 1 and {MAX_PASSWORD_COUNT}.")
            continue

        return password_count


def get_yes_no(prompt: str, default: bool = True) -> bool:
    option = "[Y/n]" if default else "[y/N]"

    while True:
        user_input = input(f"{prompt} {option}: ").strip().lower()

        if user_input == "":
            return default

        if user_input in {"y", "yes"}:
            return True

        if user_input in {"n", "no"}:
            return False

        print("Invalid input. Enter y or n.")


def get_character_options() -> tuple[bool, bool, bool, bool]:
    while True:
        print("\nCharacter options:")

        include_lowercase = get_yes_no("Include lowercase letters?")
        include_uppercase = get_yes_no("Include uppercase letters?")
        include_digits = get_yes_no("Include digits?")
        include_symbols = get_yes_no("Include symbols?")

        options = (
            include_lowercase,
            include_uppercase,
            include_digits,
            include_symbols,
        )

        if any(options):
            return options

        print("At least one character type must be enabled.")


def build_alphabet(
    include_lowercase: bool,
    include_uppercase: bool,
    include_digits: bool,
    include_symbols: bool,
    exclude_ambiguous: bool = False,
) -> str:
    alphabet = ""

    if include_lowercase:
        alphabet += string.ascii_lowercase

    if include_uppercase:
        alphabet += string.ascii_uppercase

    if include_digits:
        alphabet += string.digits

    if include_symbols:
        alphabet += string.punctuation

    if exclude_ambiguous:
        alphabet = "".join(
            character for character in alphabet if character not in AMBIGUOUS_CHARACTERS
        )

    return alphabet


def is_valid_password(
    password: str,
    include_lowercase: bool = True,
    include_uppercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
) -> bool:
    if include_lowercase and not any(c.islower() for c in password):
        return False

    if include_uppercase and not any(c.isupper() for c in password):
        return False

    if include_digits and sum(c.isdigit() for c in password) < MIN_DIGITS:
        return False

    return not include_symbols or any(c in string.punctuation for c in password)


def generate_password(
    length: int,
    include_lowercase: bool = True,
    include_uppercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    alphabet = build_alphabet(
        include_lowercase,
        include_uppercase,
        include_digits,
        include_symbols,
        exclude_ambiguous,
    )

    if not alphabet:
        raise ValueError("At least one character type must be enabled.")

    required_length = (
        int(include_lowercase)
        + int(include_uppercase)
        + (MIN_DIGITS if include_digits else 0)
        + int(include_symbols)
    )

    if length < required_length:
        raise ValueError("Password length is too short for the selected requirements.")

    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))

        if is_valid_password(
            password,
            include_lowercase,
            include_uppercase,
            include_digits,
            include_symbols,
        ):
            return password


def main(argv: list[str] | None = None) -> None:
    args = parse_arguments(argv)

    password_length = args.length if args.length is not None else get_password_length()

    password_count = args.count if args.count is not None else get_password_count()

    character_options_from_cli = any(
        (
            args.no_lowercase,
            args.no_uppercase,
            args.no_digits,
            args.no_symbols,
        )
    )

    if character_options_from_cli:
        include_lowercase = not args.no_lowercase
        include_uppercase = not args.no_uppercase
        include_digits = not args.no_digits
        include_symbols = not args.no_symbols
    else:
        (
            include_lowercase,
            include_uppercase,
            include_digits,
            include_symbols,
        ) = get_character_options()

    exclude_ambiguous = (
        True
        if args.exclude_ambiguous
        else get_yes_no(
            "Exclude ambiguous characters?",
            default=False,
        )
    )

    if password_count == 1:
        password = generate_password(
            password_length,
            include_lowercase,
            include_uppercase,
            include_digits,
            include_symbols,
            exclude_ambiguous,
        )

        if args.raw:
            print(password)
        else:
            print(f"\nPassword: {password}")

    else:
        if not args.raw:
            print("\nPasswords:")

        for index in range(1, password_count + 1):
            password = generate_password(
                password_length,
                include_lowercase,
                include_uppercase,
                include_digits,
                include_symbols,
                exclude_ambiguous,
            )

            if args.raw:
                print(password)
            else:
                print(f"{index}. {password}")


if __name__ == "__main__":
    main()
