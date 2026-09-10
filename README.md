# Password Generator

A simple and secure password generator written in Python.

## Features

- Generates a 20-character password
- Uses cryptographically secure randomness with `secrets`
- Includes lowercase letters
- Includes uppercase letters
- Includes digits
- Includes punctuation symbols
- Ensures at least:
  - 1 lowercase letter
  - 1 uppercase letter
  - 3 digits
  - 1 symbol

## Requirements

- Python 3

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

Example output:
```bash
>wc.lF~=2G.C%)m>q38W
```
Each execution generates a new password.

## Security

This project uses Python's secrets module instead of random.

The secrets module is used for generating cryptographically strong random numbers suitable for managing data such as passwords, account authentication, security tokens, and related secrets.

Official Python documentation:

[Python secrets documentation](https://docs.python.org/3/library/secrets.html)

## LICENSE

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
