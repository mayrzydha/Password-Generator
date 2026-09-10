import secrets
import string

ALPHABET: str = string.ascii_letters + string.digits + string.punctuation
PASSWORD_LENGTH: int = 20

while True:
    password: str = "".join(
        secrets.choice(ALPHABET) for _ in range(PASSWORD_LENGTH)
    )

    if (
        any(c.islower() for c in password)
        and any(c.isupper() for c in password)
        and sum(c.isdigit() for c in password) >= 3
        and any(c in string.punctuation for c in password)
    ):
        break

print(password)
