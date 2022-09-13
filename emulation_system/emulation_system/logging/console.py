from __future__ import annotations

import os
from typing import Any, Dict, List, Tuple, cast

from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.pretty import pretty_repr

from emulation_system.consts import ROOT_DIR

CONSOLE_OUTPUT_HTML_FILE_PATH = os.path.join(ROOT_DIR, "compose_file_creator_log.html")
CONSOLE_OUTPUT_TEXT_FILE_PATH = os.path.join(ROOT_DIR, "compose_file_creator_log.txt")
TOP_LEVEL_HEADER_STYLE_STRING = "bold blue underline"
SECOND_LEVEL_HEADER_STYLE_STRING = "bold yellow encircle"


def _combine_regex(*regexes: str) -> str:
    """Combine a number of regexes in to a single regex.

    Returns:
        str: New regex with all regexes ORed together.
    """
    return "|".join(regexes)


class CustomHightlighter(RegexHighlighter):
    """Highlights the text typically produced from ``__repr__`` methods.

    Copied from site-packages/rich/highlighter.ReprHighlighter
    """

    base_style = "repr."
    highlights = [
        r"(?P<tag_start><)(?P<tag_name>[-\w.:|]*)(?P<tag_contents>[\w\W]*?)(?P<tag_end>>)",
        r'(?P<attrib_name>[\w_]{1,50})=(?P<attrib_value>"?[\w_]+"?)?',
        r"(?P<brace>[][{}()])",
        _combine_regex(
            r"(?P<ipv4>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})",
            r"(?P<ipv6>([A-Fa-f0-9]{1,4}::?){1,7}[A-Fa-f0-9]{1,4})",
            r"(?P<eui64>(?:[0-9A-Fa-f]{1,2}-){7}[0-9A-Fa-f]{1,2}|(?:[0-9A-Fa-f]{1,2}:){7}[0-9A-Fa-f]{1,2}|(?:[0-9A-Fa-f]{4}\.){3}[0-9A-Fa-f]{4})",
            r"(?P<eui48>(?:[0-9A-Fa-f]{1,2}-){5}[0-9A-Fa-f]{1,2}|(?:[0-9A-Fa-f]{1,2}:){5}[0-9A-Fa-f]{1,2}|(?:[0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4})",
            r"(?P<uuid>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})",
            r"(?P<call>[\w.]*?)\(",
            r"\b(?P<bool_true>True)\b|\b(?P<bool_false>False)\b|\b(?P<none>None)\b",
            r"(?P<ellipsis>\.\.\.)",
            r"(?P<number_complex>(?<!\w)(?:\-?[0-9]+\.?[0-9]*(?:e[-+]?\d+?)?)(?:[-+](?:[0-9]+\.?[0-9]*(?:e[-+]?\d+)?))?j)",
            # r"(?P<number>(?<!\w)\-?[0-9]+\.?[0-9]*(e[-+]?\d+?)?\b|0x[0-9a-fA-F]*)",  # Don't want to highlight numbers
            r"(?P<path>\B(/[-\w._+]+)*\/)(?P<filename>[-\w._+]*)?",
            r"(?<![\\\w])(?P<str>b?'''.*?(?<!\\)'''|b?'.*?(?<!\\)'|b?\"\"\".*?(?<!\\)\"\"\"|b?\".*?(?<!\\)\")",
            r"(?P<url>(file|https|http|ws|wss)://[-0-9a-zA-Z$_+!`(),.?/;:&=%#]*)",
        ),
    ]


class CustomConsole(Console):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def header_print(self, *objects, **kwargs) -> None:
        """Adds header styling to passed string.

        Will not override any styles passed with style kwarg. Instead it will
        append the style.
        """
        if "style" in kwargs:
            split_styles = TOP_LEVEL_HEADER_STYLE_STRING.split(" ")
            split_styles.extend(kwargs["style"].split(" "))
            kwargs["style"] = " ".join(split_styles)
        else:
            kwargs["style"] = TOP_LEVEL_HEADER_STYLE_STRING
        self.print(*objects, **kwargs, sep="\n")

    def tabbed_print(self, *objects, **kwargs) -> None:
        """Adds a tab character to all passed strings."""
        objects = cast(Tuple, ["\t" + obj for obj in objects])  # casting for typing

        self.print(*objects, **kwargs, sep="\n")

    def tabbed_header_print(self, *objects, **kwargs):
        objects = cast(Tuple, ["\t" + obj for obj in objects])  # casting for typing
        self.print(*objects, **kwargs, sep="\n", style=SECOND_LEVEL_HEADER_STYLE_STRING)

    def double_tabbed_print(self, *objects, **kwargs) -> None:
        """Adds a tab character to all passed strings."""
        objects = cast(Tuple, ["\t\t" + obj for obj in objects])

        self.print(*objects, **kwargs, sep="\n")

    @staticmethod
    def convert_dict(dict_to_convert: Dict[str, Any]) -> List[str]:
        return pretty_repr(dict_to_convert).split("\n")


logging_console = CustomConsole(
    width=200,
    record=True,
    highlighter=CustomHightlighter(),
    file=open(CONSOLE_OUTPUT_TEXT_FILE_PATH, "wt"),
)
