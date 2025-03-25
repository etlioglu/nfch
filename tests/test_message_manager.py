"""Provide tests for the MessageManager class."""

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
