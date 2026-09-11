import secrets
import string

DEFAULT_LENGTH: int = 20
MIN_LENGTH: int = 15

ALPHABET: str = string.ascii_letters + string.digits + string.punctuation


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


def is_valid_password(password: str) -> bool:
    return (
        any(c.islower() for c in password)
        and any(c.isupper() for c in password)
        and sum(c.isdigit() for c in password) >= 3
        and any(c in string.punctuation for c in password)
    )


def generate_password(length: int) -> str:
    while True:
        password: str = "".join(
            secrets.choice(ALPHABET)
            for _ in range(length)
        )

        if is_valid_password(password):
            return password


def main() -> None:
    password_length = get_password_length()
    password = generate_password(password_length)

    print(password)


if __name__ == "__main__":
    main()
