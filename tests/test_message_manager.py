"""Provide tests for the MessageManager class."""

import pytest

from nfch.message_manager import MessageManager


def test__format_message() -> None:
    """Test the FileManager()._format_message abstract method."""
    input_message: str = """
        first line of the multiline message
        second line of the multiline message
        """

    expected_message: str = "first line of the multiline message\nsecond line of the multiline message"

    formatted_message = MessageManager._format_message(message=input_message)  # noqa: SLF001

    assert formatted_message == expected_message


@pytest.mark.parametrize(
    argnames=("input_message", "expected_output"),
    argvalues=[
        ("   Single line message.   ", "Single line message."),
        (
            """
            Multi-line message.
            With indentation.
            """,
            "Multi-line message.\nWith indentation.",
        ),
        ("", ""),  # Empty string
        ("   ", ""),  # String with only whitespace
    ],
)
def test__format_message_edge_cases(input_message: str, expected_output: str) -> None:
    """Test the _format_message method with various edge cases."""
    assert MessageManager._format_message(message=input_message) == expected_output  # noqa: SLF001
