import string
import unittest
from unittest.mock import MagicMock, patch

from main import (
    ALPHABET,
    AMBIGUOUS_CHARACTERS,
    DEFAULT_LENGTH,
    MIN_LENGTH,
    build_alphabet,
    generate_password,
    get_character_options,
    get_password_length,
    get_yes_no,
    is_valid_password,
    DEFAULT_PASSWORD_COUNT,
    MAX_PASSWORD_COUNT,
    get_password_count,
    main,
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
                side_effect=[
                    "abc",
                    str(MIN_LENGTH - 1),
                    "17",
                ],
            ),
            patch("builtins.print"),
        ):
            self.assertEqual(
                get_password_length(),
                17,
            )


class TestGetPasswordCount(unittest.TestCase):
    @patch("builtins.input", return_value="")
    def test_empty_input_uses_default(
        self,
        _mock_input: MagicMock,
    ) -> None:
        self.assertEqual(
            get_password_count(),
            DEFAULT_PASSWORD_COUNT,
        )

    @patch("builtins.input", return_value="5")
    def test_accepts_valid_count(
        self,
        _mock_input: MagicMock,
    ) -> None:
        self.assertEqual(
            get_password_count(),
            5,
        )

    def test_retries_until_count_is_valid(self) -> None:
        with (
            patch(
                "builtins.input",
                side_effect=[
                    "abc",
                    "0",
                    str(MAX_PASSWORD_COUNT + 1),
                    "3",
                ],
            ),
            patch("builtins.print"),
        ):
            self.assertEqual(
                get_password_count(),
                3,
            )


class TestGetYesNo(unittest.TestCase):
    @patch("builtins.input", return_value="")
    def test_empty_input_uses_default(
        self,
        _mock_input: MagicMock,
    ) -> None:
        self.assertTrue(
            get_yes_no("Test?")
        )

    @patch("builtins.input", return_value="n")
    def test_accepts_no(
        self,
        _mock_input: MagicMock,
    ) -> None:
        self.assertFalse(
            get_yes_no("Test?")
        )

    @patch("builtins.input", return_value="")
    def test_empty_input_uses_false_default(
    self,
    _mock_input: MagicMock,
) -> None:
     self.assertFalse(
        get_yes_no(
            "Test?",
            default=False,
        )
    )

    def test_retries_invalid_input(self) -> None:
        with (
            patch(
                "builtins.input",
                side_effect=["maybe", "yes"],
            ),
            patch("builtins.print"),
        ):
            self.assertTrue(
                get_yes_no("Test?")
            )


class TestGetCharacterOptions(unittest.TestCase):
    def test_defaults_to_all_enabled(self) -> None:
        with (
            patch(
                "builtins.input",
                side_effect=["", "", "", ""],
            ),
            patch("builtins.print"),
        ):
            self.assertEqual(
                get_character_options(),
                (True, True, True, True),
            )

    def test_accepts_custom_options(self) -> None:
        with (
            patch(
                "builtins.input",
                side_effect=["y", "n", "y", "n"],
            ),
            patch("builtins.print"),
        ):
            self.assertEqual(
                get_character_options(),
                (True, False, True, False),
            )

    def test_retries_when_all_are_disabled(self) -> None:
        with (
            patch(
                "builtins.input",
                side_effect=[
                    "n",
                    "n",
                    "n",
                    "n",
                    "",
                    "",
                    "",
                    "",
                ],
            ),
            patch("builtins.print"),
        ):
            self.assertEqual(
                get_character_options(),
                (True, True, True, True),
            )


class TestBuildAlphabet(unittest.TestCase):
    def test_builds_selected_alphabet(self) -> None:
        alphabet = build_alphabet(
            True,
            False,
            True,
            False,
        )

        self.assertEqual(
            alphabet,
            string.ascii_lowercase + string.digits,
        )

    def test_excludes_ambiguous_characters(self) -> None:
        alphabet: str = build_alphabet(
            True,
            True,
            True,
            True,
            exclude_ambiguous=True,
        )

        self.assertFalse(
            any(
                character in alphabet
                for character in AMBIGUOUS_CHARACTERS
            )
        )

class TestIsValidPassword(unittest.TestCase):
    def test_valid_password(self) -> None:
        self.assertTrue(
            is_valid_password("abcABC123!")
        )

    def test_missing_lowercase(self) -> None:
        self.assertFalse(
            is_valid_password("ABCXYZ123!")
        )

    def test_missing_uppercase(self) -> None:
        self.assertFalse(
            is_valid_password("abcxyz123!")
        )

    def test_missing_digits(self) -> None:
        self.assertFalse(
            is_valid_password("abcABCxyz!")
        )

    def test_fewer_than_three_digits(self) -> None:
        self.assertFalse(
            is_valid_password("abcABC12!")
        )

    def test_missing_symbol(self) -> None:
        self.assertFalse(
            is_valid_password("abcABC123")
        )

    def test_valid_with_only_lowercase_enabled(self) -> None:
        self.assertTrue(
            is_valid_password(
                "abcdefghijklmno",
                include_lowercase=True,
                include_uppercase=False,
                include_digits=False,
                include_symbols=False,
            )
        )


class TestGeneratePassword(unittest.TestCase):
    def test_generates_requested_length(self) -> None:
        for length in (
            MIN_LENGTH,
            DEFAULT_LENGTH,
            32,
        ):
            with self.subTest(length=length):
                password = generate_password(length)

                self.assertEqual(
                    len(password),
                    length,
                )

    def test_generates_valid_password(self) -> None:
        password = generate_password(DEFAULT_LENGTH)

        self.assertTrue(
            is_valid_password(password)
        )

    def test_uses_only_allowed_characters(self) -> None:
        password = generate_password(DEFAULT_LENGTH)

        self.assertTrue(
            all(
                character in ALPHABET
                for character in password
            )
        )

    def test_generates_lowercase_and_digits_only(
        self,
    ) -> None:
        password = generate_password(
            DEFAULT_LENGTH,
            include_lowercase=True,
            include_uppercase=False,
            include_digits=True,
            include_symbols=False,
        )

        allowed = (
            string.ascii_lowercase
            + string.digits
        )

        self.assertTrue(
            all(
                character in allowed
                for character in password
            )
        )

        self.assertTrue(
            is_valid_password(
                password,
                include_lowercase=True,
                include_uppercase=False,
                include_digits=True,
                include_symbols=False,
            )
        )

    def test_rejects_no_character_types(self) -> None:
        with self.assertRaises(ValueError):
            generate_password(
                DEFAULT_LENGTH,
                False,
                False,
                False,
                False,
            )

    def test_excludes_ambiguous_characters(self) -> None:
        password: str = generate_password(
            DEFAULT_LENGTH,
            exclude_ambiguous=True,
        )

        self.assertFalse(
            any(
                character in password
                for character in AMBIGUOUS_CHARACTERS
            )
        )


class TestMain(unittest.TestCase):
    def test_generates_single_password(self) -> None:
        with (
            patch(
                "builtins.input",
                side_effect=["", "", "", "", "", "", ""],
            ),
            patch(
                "main.generate_password",
                return_value="TestPassword123!",
            ) as mock_generate,
            patch("builtins.print") as mock_print,
        ):
            main()

        mock_generate.assert_called_once_with(
            DEFAULT_LENGTH,
            True,
            True,
            True,
            True,
            False,
        )

        mock_print.assert_any_call(
            "\nPassword: TestPassword123!"
        )

    def test_generates_multiple_passwords(self) -> None:
        with (
            patch(
                "builtins.input",
                side_effect=["", "3", "", "", "", "", ""],
            ),
            patch(
                "main.generate_password",
                side_effect=[
                    "PasswordOne",
                    "PasswordTwo",
                    "PasswordThree",
                ],
            ) as mock_generate,
            patch("builtins.print") as mock_print,
        ):
            main()

        self.assertEqual(
            mock_generate.call_count,
            3,
        )

        mock_print.assert_any_call("\nPasswords:")
        mock_print.assert_any_call("1. PasswordOne")
        mock_print.assert_any_call("2. PasswordTwo")
        mock_print.assert_any_call("3. PasswordThree")


if __name__ == "__main__":
    unittest.main()
