import secrets
import string

DEFAULT_LENGTH: int = 20
MIN_LENGTH: int = 15
MIN_DIGITS: int = 3

ALPHABET: str = (
    string.ascii_letters
    + string.digits
    + string.punctuation
)


def get_password_length() -> int:
    while True:
        user_input: str = input(
            f"Password length [{DEFAULT_LENGTH}]: "
        ).strip()

        if user_input == "":
            return DEFAULT_LENGTH

        try:
            password_length = int(user_input)
        except ValueError:
            print("Invalid input. Enter a whole number.")
            continue

        if password_length < MIN_LENGTH:
            print(
                f"Password must be at least "
                f"{MIN_LENGTH} characters."
            )
            continue

        return password_length


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

        include_lowercase = get_yes_no(
            "Include lowercase letters?"
        )
        include_uppercase = get_yes_no(
            "Include uppercase letters?"
        )
        include_digits = get_yes_no(
            "Include digits?"
        )
        include_symbols = get_yes_no(
            "Include symbols?"
        )

        options = (
            include_lowercase,
            include_uppercase,
            include_digits,
            include_symbols,
        )

        if any(options):
            return options

        print(
            "At least one character type must be enabled."
        )


def build_alphabet(
    include_lowercase: bool,
    include_uppercase: bool,
    include_digits: bool,
    include_symbols: bool,
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

    return alphabet


def is_valid_password(
    password: str,
    include_lowercase: bool = True,
    include_uppercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
) -> bool:
    if (
        include_lowercase
        and not any(c.islower() for c in password)
    ):
        return False

    if (
        include_uppercase
        and not any(c.isupper() for c in password)
    ):
        return False

    if (
        include_digits
        and sum(c.isdigit() for c in password) < MIN_DIGITS
    ):
        return False

    if (
        include_symbols
        and not any(c in string.punctuation for c in password)
    ):
        return False

    return True


def generate_password(
    length: int,
    include_lowercase: bool = True,
    include_uppercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
) -> str:
    alphabet = build_alphabet(
        include_lowercase,
        include_uppercase,
        include_digits,
        include_symbols,
    )

    if not alphabet:
        raise ValueError(
            "At least one character type must be enabled."
        )

    required_length = (
        int(include_lowercase)
        + int(include_uppercase)
        + (MIN_DIGITS if include_digits else 0)
        + int(include_symbols)
    )

    if length < required_length:
        raise ValueError(
            "Password length is too short "
            "for the selected requirements."
        )

    while True:
        password = "".join(
            secrets.choice(alphabet)
            for _ in range(length)
        )

        if is_valid_password(
            password,
            include_lowercase,
            include_uppercase,
            include_digits,
            include_symbols,
        ):
            return password


def main() -> None:
    password_length = get_password_length()

    (
        include_lowercase,
        include_uppercase,
        include_digits,
        include_symbols,
    ) = get_character_options()

    password = generate_password(
        password_length,
        include_lowercase,
        include_uppercase,
        include_digits,
        include_symbols,
    )

    print(f"\nPassword: {password}")


if __name__ == "__main__":
    main()
