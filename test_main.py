import unittest
from unittest.mock import MagicMock, patch

from main import (
    ALPHABET,
    DEFAULT_LENGTH,
    MIN_LENGTH,
    generate_password,
    get_password_length,
    is_valid_password,
)


class TestIsValidPassword(unittest.TestCase):
    def test_valid_password(self) -> None:
        self.assertTrue(is_valid_password("abcABC123!"))

    def test_missing_lowercase(self) -> None:
        self.assertFalse(is_valid_password("ABCXYZ123!"))

    def test_missing_uppercase(self) -> None:
        self.assertFalse(is_valid_password("abcxyz123!"))

    def test_missing_digits(self) -> None:
        self.assertFalse(is_valid_password("abcABCxyz!"))

    def test_fewer_than_three_digits(self) -> None:
        self.assertFalse(is_valid_password("abcABC12!"))

    def test_missing_symbol(self) -> None:
        self.assertFalse(is_valid_password("abcABC123"))


class TestGeneratePassword(unittest.TestCase):
    def test_generates_requested_length(self) -> None:
        for length in (MIN_LENGTH, DEFAULT_LENGTH, 32):
            with self.subTest(length=length):
                password = generate_password(length)

                self.assertEqual(len(password), length)

    def test_generates_valid_password(self) -> None:
        password = generate_password(DEFAULT_LENGTH)

        self.assertTrue(is_valid_password(password))

    def test_uses_only_allowed_characters(self) -> None:
        password = generate_password(DEFAULT_LENGTH)

        self.assertTrue(
            all(character in ALPHABET for character in password)
        )


class TestGetPasswordLength(unittest.TestCase):
    @patch("builtins.input", return_value="")
    def test_empty_input_uses_default(
        self,
        _mock_input: MagicMock,
    ) -> None:
        self.assertEqual(
            get_password_length(),
            DEFAULT_LENGTH,
        )

    @patch("builtins.input", return_value="32")
    def test_accepts_valid_length(
        self,
        _mock_input: MagicMock,
    ) -> None:
        self.assertEqual(
            get_password_length(),
            32,
        )

    @patch("builtins.input", return_value=str(MIN_LENGTH))
    def test_accepts_minimum_length(
        self,
        _mock_input: MagicMock,
    ) -> None:
        self.assertEqual(
            get_password_length(),
            MIN_LENGTH,
        )

    def test_retries_until_input_is_valid(self) -> None:
        with (
            patch(
                "builtins.input",
                side_effect=["abc", str(MIN_LENGTH - 1), "17"],
            ),
            patch("builtins.print"),
        ):
            self.assertEqual(
                get_password_length(),
                17,
            )


if __name__ == "__main__":
    unittest.main()
