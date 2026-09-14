import string
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

from main import (
    ALPHABET,
    AMBIGUOUS_CHARACTERS,
    DEFAULT_LENGTH,
    DEFAULT_PASSWORD_COUNT,
    MAX_PASSWORD_COUNT,
    MIN_LENGTH,
    VERSION,
    build_alphabet,
    generate_password,
    get_character_options,
    get_password_count,
    get_password_length,
    get_yes_no,
    is_valid_password,
    main,
    parse_arguments,
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


class TestParseArguments(unittest.TestCase):
    def test_accepts_length_and_count(self) -> None:
        args = parse_arguments(
            [
                "--length",
                "24",
                "--count",
                "3",
            ]
        )

        self.assertEqual(args.length, 24)
        self.assertEqual(args.count, 3)

    def test_rejects_disabling_all_character_types(self) -> None:
        with (
            patch("sys.stderr"),
            self.assertRaises(SystemExit),
        ):
            parse_arguments(
                [
                    "--no-lowercase",
                    "--no-uppercase",
                    "--no-digits",
                    "--no-symbols",
                ]
            )

    def test_accepts_exclude_ambiguous(self) -> None:
        args = parse_arguments(["--exclude-ambiguous"])

        self.assertTrue(args.exclude_ambiguous)

    def test_accepts_character_type_options(self) -> None:
        args = parse_arguments(
            [
                "--no-uppercase",
                "--no-symbols",
            ]
        )

        self.assertFalse(args.no_lowercase)
        self.assertTrue(args.no_uppercase)
        self.assertFalse(args.no_digits)
        self.assertTrue(args.no_symbols)

    def test_omitted_options_are_none(self) -> None:
        args = parse_arguments([])

        self.assertIsNone(args.length)
        self.assertIsNone(args.count)
        self.assertFalse(args.exclude_ambiguous)

        self.assertFalse(args.no_lowercase)
        self.assertFalse(args.no_uppercase)
        self.assertFalse(args.no_digits)
        self.assertFalse(args.no_symbols)
        self.assertFalse(args.raw)

    def test_rejects_short_length(self) -> None:
        with (
            patch("sys.stderr"),
            self.assertRaises(SystemExit),
        ):
            parse_arguments(
                [
                    "--length",
                    str(MIN_LENGTH - 1),
                ]
            )

    def test_rejects_invalid_count(self) -> None:
        with (
            patch("sys.stderr"),
            self.assertRaises(SystemExit),
        ):
            parse_arguments(
                [
                    "--count",
                    str(MAX_PASSWORD_COUNT + 1),
                ]
            )

    def test_version_exits_successfully(self) -> None:
        with (
            patch("sys.stdout", new_callable=StringIO) as mock_stdout,
            self.assertRaises(SystemExit) as context,
        ):
            parse_arguments(["--version"])

        self.assertEqual(context.exception.code, 0)
        self.assertIn(VERSION, mock_stdout.getvalue())

    def test_accepts_raw_output(self) -> None:
        args = parse_arguments(["--raw"])

        self.assertTrue(args.raw)


class TestGetYesNo(unittest.TestCase):
    @patch("builtins.input", return_value="")
    def test_empty_input_uses_default(
        self,
        _mock_input: MagicMock,
    ) -> None:
        self.assertTrue(get_yes_no("Test?"))

    @patch("builtins.input", return_value="n")
    def test_accepts_no(
        self,
        _mock_input: MagicMock,
    ) -> None:
        self.assertFalse(get_yes_no("Test?"))

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
            self.assertTrue(get_yes_no("Test?"))


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
            any(character in alphabet for character in AMBIGUOUS_CHARACTERS)
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

        self.assertTrue(is_valid_password(password))

    def test_uses_only_allowed_characters(self) -> None:
        password = generate_password(DEFAULT_LENGTH)

        self.assertTrue(all(character in ALPHABET for character in password))

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

        allowed = string.ascii_lowercase + string.digits

        self.assertTrue(all(character in allowed for character in password))

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
            any(character in password for character in AMBIGUOUS_CHARACTERS)
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
            main([])

        mock_generate.assert_called_once_with(
            DEFAULT_LENGTH,
            True,
            True,
            True,
            True,
            False,
        )

        mock_print.assert_any_call("\nPassword: TestPassword123!")

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
            main([])

        self.assertEqual(
            mock_generate.call_count,
            3,
        )

        mock_print.assert_any_call("\nPasswords:")
        mock_print.assert_any_call("1. PasswordOne")
        mock_print.assert_any_call("2. PasswordTwo")
        mock_print.assert_any_call("3. PasswordThree")

    def test_uses_command_line_length_and_count(self) -> None:
        with (
            patch(
                "builtins.input",
                side_effect=["", "", "", "", ""],
            ) as mock_input,
            patch(
                "main.generate_password",
                side_effect=[
                    "PasswordOne",
                    "PasswordTwo",
                ],
            ) as mock_generate,
            patch("builtins.print"),
        ):
            main(
                [
                    "--length",
                    "24",
                    "--count",
                    "2",
                ]
            )

        self.assertEqual(mock_input.call_count, 5)
        self.assertEqual(mock_generate.call_count, 2)

        mock_generate.assert_any_call(
            24,
            True,
            True,
            True,
            True,
            False,
        )

    def test_uses_command_line_exclude_ambiguous(self) -> None:
        with (
            patch(
                "builtins.input",
                side_effect=["", "", "", "", ""],
            ) as mock_input,
            patch(
                "main.generate_password",
                return_value="TestPassword234!",
            ) as mock_generate,
            patch("builtins.print"),
        ):
            main(
                [
                    "--length",
                    "24",
                    "--exclude-ambiguous",
                ]
            )

        self.assertEqual(mock_input.call_count, 5)

        mock_generate.assert_called_once_with(
            24,
            True,
            True,
            True,
            True,
            True,
        )

    def test_uses_command_line_character_options(self) -> None:
        with (
            patch("builtins.input") as mock_input,
            patch(
                "main.generate_password",
                return_value="test123password",
            ) as mock_generate,
            patch("builtins.print"),
        ):
            main(
                [
                    "--length",
                    "24",
                    "--count",
                    "1",
                    "--no-uppercase",
                    "--no-symbols",
                    "--exclude-ambiguous",
                ]
            )

        mock_input.assert_not_called()

        mock_generate.assert_called_once_with(
            24,
            True,
            False,
            True,
            False,
            True,
        )

    def test_uses_raw_output(self) -> None:
        with (
            patch("builtins.input") as mock_input,
            patch(
                "main.generate_password",
                side_effect=[
                    "PasswordOne",
                    "PasswordTwo",
                ],
            ),
            patch("builtins.print") as mock_print,
        ):
            main(
                [
                    "--length",
                    "24",
                    "--count",
                    "2",
                    "--raw",
                    "--no-uppercase",
                    "--no-symbols",
                    "--exclude-ambiguous",
                ]
            )

        mock_input.assert_not_called()

        self.assertEqual(mock_print.call_count, 2)
        mock_print.assert_any_call("PasswordOne")
        mock_print.assert_any_call("PasswordTwo")


if __name__ == "__main__":
    unittest.main()
