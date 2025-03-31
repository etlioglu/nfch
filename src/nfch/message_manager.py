"""Module contatining the class MessageManager managing colored output messages."""

from rich import print as rich_print


class MessageManager:
    """A utility class for printing colored messages."""

    @staticmethod
    def echo(message: str, message_type: str = "info", level: int = 0) -> None:
        """Print a colored and optionally indented message based on message type.

        Parameters
        ----------
        message : str
            Text message to be printed
        message_type : str, optional
            One of five types; info (yellow), process (blue), success (green), warning (orange) and fail (red), by
            default "info"
        level : int, optional
            The larger the level the more indented is the message, by default 0

        """
        colors: dict[str, str] = {
            "info": "[yellow]",
            "process": "[blue]",
            "success": "[green]",
            "warning": "[orange1]",
            "fail": "[red]",
        }
        new_line: str = "\n"
        color: str = colors[message_type]
        indentation: str = ""
        emoticon: str = ""
        if level != 0:
            new_line = ""
            indentation: str = " " * level
            emoticon = ":arrow_right_hook: "

        rich_print(f"{new_line}{color}{indentation + emoticon + message}{color}")
