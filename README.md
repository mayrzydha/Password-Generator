# Password Generator

[![Tests](https://github.com/mayrzydha/Password-Generator/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/mayrzydha/Password-Generator/actions/workflows/tests.yml)

A simple Python password generator using cryptographically secure randomness.

## Features

- Uses cryptographically secure randomness with `secrets`
- Configurable password length
- Default password length: 20 characters
- Minimum password length: 15 characters
- Selectable character types:
  - Lowercase letters
  - Uppercase letters
  - Digits
  - Symbols
- All character types are enabled by default
- Prevents all character types from being disabled
- Ensures selected character requirements are satisfied
- Requires at least 3 digits when digits are enabled
- Validates user input
- Includes automated tests using Python's `unittest`
- No third-party packages are required
- Option to exclude ambiguous characters (`0`, `O`, `1`, `l`, `I`)
- Generate multiple passwords in a single run
- Generates 1 password by default
- Supports up to 100 passwords per run
- Supports command-line arguments alongside interactive prompts

## Requirements

- Python 3.14

No third-party packages are required.

## Usage

Clone the repository:

```bash
git clone https://github.com/mayrzydha/Password-Generator.git
```

Move into the project directory:
```bash
cd Password-Generator
```

Run the program:
```bash
python main.py
```

Example:

```text
Password length [20]: 24
Number of passwords [1]: 3

Character options:
Include lowercase letters? [Y/n]:
Include uppercase letters? [Y/n]:
Include digits? [Y/n]:
Include symbols? [Y/n]:
Exclude ambiguous characters? [y/N]: y

Passwords:
1. ...
2. ...
3. ...
```

Press Enter to use the default password length and enable a character type by default.

### Command-Line Options

View all available options:

```bash
python main.py --help
```

Available options:

- `--length LENGTH` — Set the password length. Minimum: 15.
- `--count COUNT` — Set the number of passwords to generate. Range: 1–100.
- `--exclude-ambiguous` — Exclude ambiguous characters: `0`, `O`, `1`, `l`, `I`.
- `--no-lowercase` — Exclude lowercase letters.
- `--no-uppercase` — Exclude uppercase letters.
- `--no-digits` — Exclude digits.
- `--no-symbols` — Exclude symbols.

Example: generate three 24-character passwords:

```bash
python main.py --length 24 --count 3
```

Example: generate two 24-character passwords without uppercase letters, symbols, or ambiguous characters:

```bash
python main.py --length 24 --count 2 --no-uppercase --no-symbols --exclude-ambiguous
```

When any `--no-*` character option is provided, character-type prompts are skipped and all character types not explicitly disabled remain enabled.

At least one character type must remain enabled.

## Testing

Run the automated test suite with:

```bash
python -m unittest -v
```

The tests cover password generation, validation, configurable character types, password length and count handling, command-line arguments, and invalid user input.

## Security

This project uses Python's secrets module instead of random.

The secrets module is used for generating cryptographically strong random numbers suitable for managing data such as passwords, account authentication, security tokens, and related secrets.

Official Python documentation:

[Python secrets documentation](https://docs.python.org/3/library/secrets.html)

## LICENSE

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
