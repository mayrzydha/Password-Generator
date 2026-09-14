# Password Generator

[![Tests](https://github.com/mayrzydha/Password-Generator/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/mayrzydha/Password-Generator/actions/workflows/tests.yml)

A cryptographically secure password generator with a Python CLI and browser-based GUI.

## Web App

Use the browser version:

[Open Password Generator](https://mayrzydha.github.io/Password-Generator/)

The web GUI runs the same Python password generator locally in the browser through Pyodide. Generated passwords are not sent to a server.

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
- No third-party packages are required for the CLI
- Option to exclude ambiguous characters (`0`, `O`, `1`, `l`, `I`)
- Generate multiple passwords in a single run
- Generates 1 password by default
- Supports up to 100 passwords per run
- Supports command-line arguments alongside interactive prompts
- Supports raw password output for scripting and pipelines
- Supports non-interactive generation with default values using `--defaults`
- Displays the current program version with `--version`
- Includes a browser-based GUI deployed with GitHub Pages
- Runs the same Python generator in the browser through Pyodide
- Supports copying individual passwords or all generated passwords from the web GUI

## Requirements

### CLI

- Python 3.14

No third-party packages are required.

### Web App

- A modern browser with JavaScript and WebAssembly support

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
- `--version` — Show the program version and exit.
- `--raw` — Print passwords only, one per line.
- `--defaults` — Use default values for unspecified options without prompting.

Example: generate three 24-character passwords:

```bash
python main.py --length 24 --count 3
```

Example: generate two 24-character passwords without uppercase letters, symbols, or ambiguous characters:

```bash
python main.py --length 24 --count 2 --no-uppercase --no-symbols --exclude-ambiguous
```

Example: generate passwords in raw output mode:

```bash
python main.py --length 24 --count 3 --raw --no-uppercase --no-symbols --exclude-ambiguous
```

Raw output prints only the generated passwords, one per line, without headings or numbering. This is useful when piping the output to another command or script.

Example: generate a password using all default values without interactive prompts:

```bash
python main.py --defaults
```

The `--defaults` option uses default values for any unspecified settings and skips interactive prompts. Explicit command-line options still override their corresponding defaults.

Example: generate a password with default settings in raw output mode:

```bash
python main.py --defaults --raw
```

View the current program version:

```bash
python main.py --version
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
